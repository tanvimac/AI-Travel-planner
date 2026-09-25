from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: Optional[str] = None


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    email: str


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: Optional[str] = None
    is_active: bool
    created_at: str


class UserPreferenceUpdate(BaseModel):
    home_currency: Optional[str] = "USD"
    language: Optional[str] = "en"
    travel_style: Optional[str] = "Mid-range"
    dietary_restrictions: Optional[str] = None
    interests: Optional[str] = None
