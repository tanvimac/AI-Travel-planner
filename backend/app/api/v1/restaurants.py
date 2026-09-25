from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.db.database import get_db
from app.core.deps import get_optional_current_user
from app.db.models.user import User
from app.db.models.travel import Restaurant, Reservation
from app.db.models.trip import Trip
from app.providers.restaurants import RestaurantProvider
from app.core.errors import NotFoundException

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])
restaurant_provider = RestaurantProvider()


class RestaurantReserveRequest(BaseModel):
    trip_id: int
    name: str = Field(..., min_length=1)
    city: str = Field(..., min_length=1)
    cuisine: str = "Regional"
    price_range: str = "$$"
    rating: Optional[float] = 4.5
    specialty: Optional[str] = None
    party_size: int = Field(default=2, ge=1)
    reservation_time: Optional[str] = None


@router.get("/search")
def search_restaurants(
    city: str = Query(..., min_length=1, description="City name to search"),
    cuisine: Optional[str] = Query(None, description="Cuisine type"),
    price_range: Optional[str] = Query(None, description="Price tier: $, $$, $$$, $$$$"),
):
    """Search dining establishments across curated culinary catalog."""
    results = restaurant_provider.search_restaurants(city=city, cuisine=cuisine, price_range=price_range)
    return {
        "status": "success",
        "city": city,
        "count": len(results),
        "restaurants": results,
    }


@router.post("/reserve", status_code=status.HTTP_201_CREATED)
def reserve_restaurant(
    payload: RestaurantReserveRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    """Record a dining reservation or selected dining place for a trip."""
    trip = db.query(Trip).filter(Trip.id == payload.trip_id).first()
    if not trip:
        raise NotFoundException(message=f"Trip with ID {payload.trip_id} not found", details={"trip_id": payload.trip_id})

    restaurant_record = Restaurant(
        trip_id=trip.id,
        name=payload.name,
        cuisine=payload.cuisine,
        city=payload.city,
        price_range=payload.price_range,
        rating=payload.rating,
        recommended_dishes={"specialty": payload.specialty} if payload.specialty else {},
    )
    db.add(restaurant_record)
    db.flush()

    reservation = Reservation(
        trip_id=trip.id,
        user_id=current_user.id if current_user else None,
        reservation_type="restaurant",
        reference_code=f"RST-{restaurant_record.id}-{trip.id}",
        provider_name="RestaurantProvider",
        status="confirmed",
        total_price=0.0,
        currency="USD",
        booking_details={
            "restaurant_id": restaurant_record.id,
            "restaurant_name": payload.name,
            "party_size": payload.party_size,
            "reservation_time": payload.reservation_time,
        },
    )
    db.add(reservation)
    db.commit()
    db.refresh(reservation)

    return {
        "status": "success",
        "message": f"Table reserved at {payload.name}",
        "reservation_id": reservation.id,
        "reference_code": reservation.reference_code,
        "restaurant": {
            "id": restaurant_record.id,
            "name": restaurant_record.name,
            "cuisine": restaurant_record.cuisine,
        },
    }
