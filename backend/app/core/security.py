import os
import hmac
import hashlib
import base64
import json
import time
from typing import Optional, Dict, Any
from app.core.config import settings

# Secret key for signing tokens
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "ai-travel-planner-super-secret-key-321-secure-jwt")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = 60 * 60 * 24 * 7 # 7 days


def hash_password(password: str) -> str:
    """Secure password hashing using PBKDF2-HMAC-SHA256 with random salt."""
    salt = os.urandom(16)
    kdf = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100_000)
    return f"{base64.b64encode(salt).decode('utf-8')}${base64.b64encode(kdf).decode('utf-8')}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify plain password against PBKDF2 hash."""
    try:
        salt_b64, kdf_b64 = hashed_password.split("$")
        salt = base64.b64decode(salt_b64.encode("utf-8"))
        expected_kdf = base64.b64decode(kdf_b64.encode("utf-8"))
        test_kdf = hashlib.pbkdf2_hmac("sha256", plain_password.encode("utf-8"), salt, 100_000)
        return hmac.compare_digest(expected_kdf, test_kdf)
    except Exception:
        return False


def create_access_token(data: Dict[str, Any], expires_delta: Optional[int] = None) -> str:
    """Create signed HMAC-SHA256 JWT token."""
    expire = time.time() + (expires_delta or ACCESS_TOKEN_EXPIRE_SECONDS)
    payload = dict(data)
    payload["exp"] = expire

    header = {"alg": ALGORITHM, "typ": "JWT"}
    header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode("utf-8")).decode("utf-8").rstrip("=")
    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode("utf-8")).decode("utf-8").rstrip("=")

    signing_input = f"{header_b64}.{payload_b64}".encode("utf-8")
    signature = hmac.new(SECRET_KEY.encode("utf-8"), signing_input, hashlib.sha256).digest()
    sig_b64 = base64.urlsafe_b64encode(signature).decode("utf-8").rstrip("=")

    return f"{header_b64}.{payload_b64}.{sig_b64}"


def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """Decode and verify HMAC-SHA256 JWT token."""
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        header_b64, payload_b64, sig_b64 = parts

        # Recompute signature
        signing_input = f"{header_b64}.{payload_b64}".encode("utf-8")
        expected_sig = hmac.new(SECRET_KEY.encode("utf-8"), signing_input, hashlib.sha256).digest()
        pad_sig = sig_b64 + "=" * (-len(sig_b64) % 4)
        actual_sig = base64.urlsafe_b64decode(pad_sig.encode("utf-8"))

        if not hmac.compare_digest(expected_sig, actual_sig):
            return None

        pad_payload = payload_b64 + "=" * (-len(payload_b64) % 4)
        payload = json.loads(base64.urlsafe_b64decode(pad_payload.encode("utf-8")).decode("utf-8"))

        if payload.get("exp", 0) < time.time():
            return None # Expired

        return payload
    except Exception:
        return None
