from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.user import User, UserPreference
from app.schemas.auth import (
    UserRegisterRequest,
    UserLoginRequest,
    TokenResponse,
    UserResponse,
    UserPreferenceUpdate,
)
from app.core.security import hash_password, verify_password, create_access_token
from app.core.errors import AppException, AuthenticationException, NotFoundException
from app.core.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(request: UserRegisterRequest, db: Session = Depends(get_db)):
    """Register a new user account and return access token."""
    existing = db.query(User).filter(User.email == request.email).first()
    if existing:
        raise AppException(
            code="USER_ALREADY_EXISTS",
            message="An account with this email address already exists.",
            status_code=status.HTTP_409_CONFLICT,
        )

    user = User(
        email=request.email,
        hashed_password=hash_password(request.password),
        full_name=request.full_name,
    )
    db.add(user)
    db.flush()

    # Create default preferences
    pref = UserPreference(user_id=user.id)
    db.add(pref)
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": str(user.id), "email": user.email})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.id,
        "email": user.email,
    }


@router.post("/login", response_model=TokenResponse)
def login(request: UserLoginRequest, db: Session = Depends(get_db)):
    """Authenticate with email and password to receive access token."""
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not verify_password(request.password, user.hashed_password):
        raise AuthenticationException("Invalid email or password.")

    if not user.is_active:
        raise AuthenticationException("User account is deactivated.")

    token = create_access_token({"sub": str(user.id), "email": user.email})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.id,
        "email": user.email,
    }


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    """Get current authenticated user profile and preferences."""
    pref = current_user.preferences
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "is_active": current_user.is_active,
        "created_at": current_user.created_at.isoformat(),
        "preferences": {
            "home_currency": pref.home_currency if pref else "USD",
            "language": pref.language if pref else "en",
            "travel_style": pref.travel_style if pref else "Mid-range",
            "dietary_restrictions": pref.dietary_restrictions if pref else None,
            "interests": pref.interests if pref else None,
        } if pref else None,
    }


@router.put("/preferences")
def update_preferences(
    request: UserPreferenceUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update preferences for the current authenticated user."""
    pref = current_user.preferences
    if not pref:
        pref = UserPreference(user_id=current_user.id)
        db.add(pref)

    if request.home_currency is not None:
        pref.home_currency = request.home_currency
    if request.language is not None:
        pref.language = request.language
    if request.travel_style is not None:
        pref.travel_style = request.travel_style
    if request.dietary_restrictions is not None:
        pref.dietary_restrictions = request.dietary_restrictions
    if request.interests is not None:
        pref.interests = request.interests

    db.commit()
    db.refresh(pref)
    return {
        "status": "success",
        "message": "Preferences updated successfully",
        "preferences": {
            "home_currency": pref.home_currency,
            "language": pref.language,
            "travel_style": pref.travel_style,
            "dietary_restrictions": pref.dietary_restrictions,
            "interests": pref.interests,
        },
    }
