from typing import Optional
from pydantic import BaseModel


class TravelRequest(BaseModel):
    destination: str
    days: int
    travelers: int
    budget: float
    interests: str
    travelStyle: Optional[str] = "Mid-range"


class TravelResponse(BaseModel):
    message: str
    destination: str
    days: int
    travelers: int
    budget: float
    interests: str
    travelStyle: Optional[str] = "Mid-range"
