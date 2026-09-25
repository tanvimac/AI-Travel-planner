from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from app.db.session import get_db
from app.db.models.travel import Flight, Reservation
from app.db.models.trip import Trip
from app.providers.flights import FlightProvider
from app.core.errors import NotFoundException

router = APIRouter(prefix="/flights", tags=["Flights"])
provider = FlightProvider()


class FlightReserveRequest(BaseModel):
    trip_id: int
    airline: str = Field(..., min_length=1)
    flight_number: str = Field(..., min_length=1)
    departure_airport: str = Field(..., min_length=2)
    arrival_airport: str = Field(..., min_length=2)
    price: float = Field(..., ge=0.0)
    currency: str = "USD"
    cabin_class: str = "Economy"


@router.get("/search")
def search_flights(
    origin: str = Query(..., min_length=2),
    destination: str = Query(..., min_length=2),
    departure_date: Optional[str] = None,
    cabin_class: str = Query(default="Economy"),
    passengers: int = Query(default=1, ge=1, le=10),
    currency: str = Query(default="USD"),
):
    """Search flight quotes, airlines, and schedules."""
    flights = provider.search_flights(
        origin=origin,
        destination=destination,
        departure_date=departure_date,
        cabin_class=cabin_class,
        currency=currency,
        passengers=passengers,
    )
    return {
        "origin": origin,
        "destination": destination,
        "cabin_class": cabin_class,
        "passengers": passengers,
        "count": len(flights),
        "flights": flights,
    }


@router.post("/reserve", status_code=status.HTTP_201_CREATED)
def reserve_flight(
    payload: FlightReserveRequest,
    db: Session = Depends(get_db),
):
    """Add a flight to trip and record a confirmed reservation."""
    trip = db.query(Trip).filter(Trip.id == payload.trip_id).first()
    if not trip:
        raise NotFoundException(resource="Trip", identifier=payload.trip_id)

    flight = Flight(
        trip_id=trip.id,
        airline=payload.airline,
        flight_number=payload.flight_number,
        departure_airport=payload.departure_airport,
        arrival_airport=payload.arrival_airport,
        price=payload.price,
        currency=payload.currency,
        cabin_class=payload.cabin_class,
        status="confirmed",
    )
    db.add(flight)
    db.flush()

    reservation = Reservation(
        trip_id=trip.id,
        reservation_type="flight",
        reference_code=payload.flight_number,
        provider_name=payload.airline,
        status="confirmed",
        total_price=payload.price,
        currency=payload.currency,
        booking_details={
            "flight_id": flight.id,
            "flight_number": payload.flight_number,
            "origin": payload.departure_airport,
            "destination": payload.arrival_airport,
            "cabin_class": payload.cabin_class,
        },
    )
    db.add(reservation)
    db.commit()
    db.refresh(reservation)

    return {
        "status": "success",
        "message": f"Flight {payload.flight_number} reserved successfully",
        "flight_id": flight.id,
        "reservation_id": reservation.id,
        "reference_code": reservation.reference_code,
        "total_price": payload.price,
        "currency": payload.currency,
    }
