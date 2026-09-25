from typing import Optional
from fastapi import Depends, Header
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.user import User
from app.core.security import decode_access_token
from app.core.errors import AuthenticationException


def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
) -> User:
    """Dependency that enforces a valid Bearer JWT token."""
    if not authorization or not authorization.startswith("Bearer "):
        raise AuthenticationException("Authorization header with Bearer token is required.")

    token = authorization.split("Bearer ", 1)[1].strip()
    payload = decode_access_token(token)
    if not payload:
        raise AuthenticationException("Invalid or expired authentication token.")

    user_id = payload.get("sub") or payload.get("user_id")
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user or not user.is_active:
        raise AuthenticationException("User account not found or deactivated.")

    return user


def get_optional_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
) -> Optional[User]:
    """Dependency that extracts user if Bearer token is provided, without failing if absent."""
    if not authorization or not authorization.startswith("Bearer "):
        return None

    try:
        token = authorization.split("Bearer ", 1)[1].strip()
        payload = decode_access_token(token)
        if not payload:
            return None
        user_id = payload.get("sub") or payload.get("user_id")
        return db.query(User).filter(User.id == int(user_id)).first()
    except Exception:
        return None
