import time
import uuid
from typing import Dict, Tuple
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from app.core.errors import RateLimitException, format_error_response
from fastapi.responses import JSONResponse


class RequestIdMiddleware(BaseHTTPMiddleware):
    """Assigns unique Request ID to each HTTP request and propagates it on response headers."""
    async def dispatch(self, request: Request, call_next):
        req_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        request.state.request_id = req_id
        response: Response = await call_next(request)
        response.headers["X-Request-ID"] = req_id
        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response


class SimpleRateLimiterMiddleware(BaseHTTPMiddleware):
    """
    Lightweight sliding-window rate limiter per client IP.
    Protects expensive AI and provider endpoints from denial of service.
    """
    def __init__(self, app, requests_per_minute: int = 120):
        super().__init__(app)
        self.rpm = requests_per_minute
        # Dictionary of ip -> (count, window_start_epoch)
        self._clients: Dict[str, Tuple[int, float]] = {}

    async def dispatch(self, request: Request, call_next):
        # Exempt health endpoints
        if request.url.path.startswith("/health") or request.method == "OPTIONS":
            return await call_next(request)

        client_ip = request.client.host if request.client else "127.0.0.1"
        now = time.time()
        count, window_start = self._clients.get(client_ip, (0, now))

        if now - window_start > 60:
            self._clients[client_ip] = (1, now)
        else:
            if count >= self.rpm:
                req_id = getattr(request.state, "request_id", str(uuid.uuid4()))
                return JSONResponse(
                    status_code=429,
                    content={
                        "error": {
                            "code": "RATE_LIMIT_EXCEEDED",
                            "message": f"Rate limit of {self.rpm} requests/min exceeded. Please slow down.",
                            "request_id": req_id,
                        }
                    },
                    headers={"Retry-After": "30", "X-Request-ID": req_id},
                )
            self._clients[client_ip] = (count + 1, window_start)

        return await call_next(request)
