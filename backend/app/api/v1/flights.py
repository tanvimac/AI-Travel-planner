from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.travel import Flight, Reservation
from app.db.models.trip import Trip
from app.providers.flights import FlightProvider
from app.core.errors import NotFoundException

router = APIRouter(prefix="/flights", tags=["Flights"])
provider = FlightProvider()


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
    trip_id: int,
    airline: str,
    flight_number: str,
    departure_airport: str,
    arrival_airport: str,
    price: float,
    currency: str = "USD",
    cabin_class: str = "Economy",
    db: Session = Depends(get_db),
):
    """Add a flight to trip and record a confirmed reservation."""
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise NotFoundException(resource="Trip", identifier=trip_id)

    flight = Flight(
        trip_id=trip.id,
        airline=airline,
        flight_number=flight_number,
        departure_airport=departure_airport,
        arrival_airport=arrival_airport,
        price=price,
        currency=currency,
        cabin_class=cabin_class,
        status="confirmed",
    )
    db.add(flight)

    reservation = Reservation(
        trip_id=trip.id,
        reservation_type="flight",
        reference_code=flight_number,
        provider_name=airline,
        status="confirmed",
        total_price=price,
        currency=currency,
        booking_details={
            "flight_number": flight_number,
            "route": f"{departure_airport} -> {arrival_airport}",
            "cabin": cabin_class,
        },
    )
    db.add(reservation)
    db.commit()
    db.refresh(flight)

    return {
        "flight_id": flight.id,
        "reservation_id": reservation.id,
        "status": "confirmed",
        "details": {
            "airline": flight.airline,
            "flight_number": flight.flight_number,
            "total_price": flight.price,
            "currency": flight.currency,
        },
    }
