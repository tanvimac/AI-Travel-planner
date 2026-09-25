from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


# --- Trips ---
class TripCreateV1Request(BaseModel):
    destination: str = Field(..., min_length=1)
    days: int = Field(default=7, ge=1, le=30)
    travelers: int = Field(default=2, ge=1, le=20)
    budget: float = Field(default=5000.0, ge=100.0)
    interests: str = Field(default="Culture, Food, Sights")
    travel_style: Optional[str] = Field(default="Mid-range", alias="travelStyle")
    currency: Optional[str] = "USD"
    start_date: Optional[str] = None
    end_date: Optional[str] = None

    class Config:
        populate_by_name = True


# --- Routes ---
class RouteRequest(BaseModel):
    origin: str
    destination: str
    mode: str = "transit" # transit, driving, walking, flight


# --- Places ---
class PlaceSearchRequest(BaseModel):
    query: str
    city: Optional[str] = None
    limit: int = 5


# --- Weather ---
class WeatherQueryRequest(BaseModel):
    city: str
    days: int = 5


# --- Currency ---
class CurrencyConvertRequest(BaseModel):
    amount: float
    from_currency: str = "USD"
    to_currency: str = "EUR"


# --- Flights ---
class FlightSearchRequest(BaseModel):
    origin: str
    destination: str
    departure_date: Optional[str] = None
    cabin_class: str = "Economy"
    passengers: int = 1
    currency: str = "USD"


# --- Hotels ---
class HotelSearchRequest(BaseModel):
    city: str
    travel_style: Optional[str] = None
    max_price: Optional[float] = None
    currency: str = "USD"


# --- Restaurants ---
class RestaurantSearchRequest(BaseModel):
    city: str
    cuisine: Optional[str] = None
    price_range: Optional[str] = None


# --- Transport ---
class TransportSearchRequest(BaseModel):
    origin: str
    destination: str
    city: Optional[str] = None


# --- Budget & Expenses ---
class BudgetSetRequest(BaseModel):
    total_budget: float
    currency: str = "USD"
    flights_allocated: Optional[float] = 0.0
    accommodation_allocated: Optional[float] = 0.0
    food_allocated: Optional[float] = 0.0
    activities_allocated: Optional[float] = 0.0
    transit_allocated: Optional[float] = 0.0
    misc_allocated: Optional[float] = 0.0


class ExpenseCreateRequest(BaseModel):
    category: str # flights, accommodation, food, activities, transit, misc
    amount: float
    currency: str = "USD"
    description: str
    paid_by: Optional[str] = None
    expense_date: Optional[str] = None


# --- Concierge ---
class ConciergeChatRequest(BaseModel):
    trip_id: Optional[int] = None
    message: str
    conversation_id: Optional[int] = None


# --- Replan ---
class ReplanRequest(BaseModel):
    trip_id: int
    change_type: str # 'budget', 'interests', 'duration', 'pace'
    new_value: Any
    reason: Optional[str] = None
