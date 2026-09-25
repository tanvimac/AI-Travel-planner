import time
import threading
import logging
from typing import Any, Optional
from google import genai
from google.genai.errors import ServerError, ClientError
from app.core.config import settings

logger = logging.getLogger("gemini_retry")

# Global timestamp of the last Gemini request start (epoch seconds).
_last_request_time: float = 0.0
_rate_limit_lock = threading.Lock()


def _get_min_interval() -> float:
    return getattr(settings, "GEMINI_MIN_INTERVAL", 1.0)


def _enforce_rate_limit() -> None:
    """Sleep if the previous request was started less than min interval seconds ago.

    Thread-safe implementation that updates the global ``_last_request_time``.
    """
    global _last_request_time
    min_interval = _get_min_interval()
    if min_interval <= 0:
        return
    with _rate_limit_lock:
        now = time.time()
        elapsed = now - _last_request_time
        if elapsed < min_interval:
            time.sleep(min_interval - elapsed)
        _last_request_time = time.time()


import re

def _extract_retry_delay(exc: Exception) -> Optional[float]:
    """Extract recommended retry delay (in seconds) from Gemini ClientError."""
    # 1. Attribute check
    retry_after = getattr(exc, "retry_after", None)
    if retry_after is not None:
        try:
            return float(retry_after)
        except (ValueError, TypeError):
            pass

    # 2. Check details list in response_json
    response_json = getattr(exc, "response_json", None)
    if isinstance(response_json, dict):
        error_dict = response_json.get("error", {})
        for detail in error_dict.get("details", []):
            if isinstance(detail, dict) and "retryDelay" in detail:
                raw = str(detail["retryDelay"]).rstrip("s")
                try:
                    return float(raw) + 1.0  # Add 1s margin
                except ValueError:
                    pass

    # 3. Regex match on exception string (e.g. 'retry in 21.04s' or 'retryDelay': '21s')
    exc_str = str(exc)
    match = re.search(r"retry in ([0-9.]+)s", exc_str, re.IGNORECASE)
    if match:
        try:
            return float(match.group(1)) + 1.0
        except ValueError:
            pass

    match2 = re.search(r"retryDelay['\"]?:\s*['\"]?([0-9.]+)s", exc_str, re.IGNORECASE)
    if match2:
        try:
            return float(match2.group(1)) + 1.0
        except ValueError:
            pass

    return None


def gemini_generate(
    client: genai.Client,
    *,
    model: str,
    contents: str,
    config: Optional[Any] = None,
    max_attempts: int = 4,
    base_delay: int = 2,
) -> Any:
    """Call Gemini ``generate_content`` with retries, rate‑limiting and 429 handling.

    * Retries on temporary ``ServerError`` with HTTP status **503** (UNAVAILABLE)
      using exponential back‑off (2 s → 4 s → 8 s).
    * Handles **429 RESOURCE_EXHAUSTED** via ``ClientError`` by sleeping for the retry
      interval suggested by the server (if any) or a safe backoff delay (at least 15s) and retrying.
    * Enforces minimum interval between consecutive Gemini calls.
    * Forwards optional ``config`` (e.g., GenerateContentConfig) to ``generate_content``.
    * All other exceptions are propagated unchanged.
    """
    attempt = 0
    kwargs: dict[str, Any] = {"model": model, "contents": contents}
    if config is not None:
        kwargs["config"] = config

    while True:
        _enforce_rate_limit()
        try:
            return client.models.generate_content(**kwargs)
        except ServerError as exc:
            status = getattr(exc, "code", getattr(exc, "status_code", None))
            if status == 503 or "503" in str(exc) or "UNAVAILABLE" in str(exc):
                attempt += 1
                if attempt >= max_attempts:
                    raise
                delay = base_delay * (2 ** (attempt - 1))
                logger.warning("ServerError 503 received; retrying in %ds (attempt %d/%d)", delay, attempt, max_attempts)
                time.sleep(delay)
                continue
            else:
                raise
        except ClientError as exc:
            status = getattr(exc, "code", getattr(exc, "status_code", None))
            if status == 429 or "429" in str(exc) or "RESOURCE_EXHAUSTED" in str(exc):
                attempt += 1
                if attempt >= max_attempts:
                    logger.error("ClientError 429: max attempts (%d) reached. Raising exception.", max_attempts)
                    raise
                retry_delay = _extract_retry_delay(exc)
                if retry_delay is None:
                    # In free tier, 429 requires waiting for quota window or at least 15s
                    retry_delay = max(_get_min_interval(), 15.0)
                logger.warning(
                    "ClientError 429 (RESOURCE_EXHAUSTED); sleeping %.1fs before retry (attempt %d/%d)",
                    retry_delay,
                    attempt,
                    max_attempts,
                )
                time.sleep(retry_delay)
                continue
            else:
                raise
