from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.db.database import get_db
from app.core.deps import get_optional_current_user
from app.db.models.user import User
from app.db.models.travel import Hotel, Reservation
from app.db.models.trip import Trip
from app.providers.hotels import HotelProvider
from app.core.errors import NotFoundException, ValidationException

router = APIRouter(prefix="/hotels", tags=["Hotels"])
hotel_provider = HotelProvider()


class HotelReserveRequest(BaseModel):
    trip_id: int
    name: str = Field(..., min_length=1)
    city: str = Field(..., min_length=1)
    price_per_night: float = Field(..., ge=0.0)
    nights: int = Field(default=1, ge=1)
    currency: str = "USD"
    rating: Optional[float] = None
    amenities: Optional[List[str]] = None


@router.get("/search")
def search_hotels(
    city: str = Query(..., min_length=1, description="City name to search"),
    style: Optional[str] = Query(None, description="Travel style: Luxury, Mid-range, Budget"),
    max_price: Optional[float] = Query(None, ge=0.0, description="Max price per night"),
    currency: str = Query("USD", description="Currency code"),
):
    """Search hotels across curated provider inventory."""
    hotels = hotel_provider.search_hotels(city=city, style=style, max_price=max_price, currency=currency)
    return {
        "status": "success",
        "city": city,
        "count": len(hotels),
        "hotels": hotels,
    }


@router.post("/reserve", status_code=status.HTTP_201_CREATED)
def reserve_hotel(
    payload: HotelReserveRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    """Reserve a hotel for a trip and record in reservation ledger."""
    trip = db.query(Trip).filter(Trip.id == payload.trip_id).first()
    if not trip:
        raise NotFoundException(message=f"Trip with ID {payload.trip_id} not found", details={"trip_id": payload.trip_id})

    total_price = round(payload.price_per_night * payload.nights, 2)
    hotel_record = Hotel(
        trip_id=trip.id,
        name=payload.name,
        city=payload.city,
        price_per_night=payload.price_per_night,
        currency=payload.currency,
        rating=payload.rating,
        amenities={"items": payload.amenities or []},
    )
    db.add(hotel_record)
    db.flush()

    reservation = Reservation(
        trip_id=trip.id,
        user_id=current_user.id if current_user else None,
        reservation_type="hotel",
        reference_code=f"HTL-{hotel_record.id}-{trip.id}",
        provider_name="HotelProvider",
        status="confirmed",
        total_price=total_price,
        currency=payload.currency,
        booking_details={
            "hotel_id": hotel_record.id,
            "hotel_name": payload.name,
            "nights": payload.nights,
            "price_per_night": payload.price_per_night,
        },
    )
    db.add(reservation)
    db.commit()
    db.refresh(reservation)

    return {
        "status": "success",
        "message": f"Hotel {payload.name} reserved successfully",
        "reservation_id": reservation.id,
        "reference_code": reservation.reference_code,
        "total_price": total_price,
        "currency": payload.currency,
    }
