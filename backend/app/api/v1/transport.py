from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.db.database import get_db
from app.core.deps import get_optional_current_user
from app.db.models.user import User
from app.db.models.travel import Route, Reservation
from app.db.models.trip import Trip
from app.providers.routes import RoutesProvider
from app.core.errors import NotFoundException

router = APIRouter(prefix="/transport", tags=["Transport"])
routes_provider = RoutesProvider()


class TransportBookRequest(BaseModel):
    trip_id: int
    origin: str = Field(..., min_length=1)
    destination: str = Field(..., min_length=1)
    mode: str = Field(default="transit", description="transit, rideshare, car_rental, train, private_transfer")
    cost: float = Field(default=25.0, ge=0.0)
    currency: str = "USD"
    notes: Optional[str] = None


@router.get("/options")
def get_transport_options(
    origin: str = Query(..., min_length=1, description="Departure location or station"),
    destination: str = Query(..., min_length=1, description="Arrival location or station"),
    city: Optional[str] = Query(None, description="City context"),
):
    """Retrieve multi-modal transport options between two locations."""
    modes = ["transit", "rideshare", "train", "rental"]
    options = []

    for mode in modes:
        plan = routes_provider.plan_route(origin=origin, destination=destination, mode=mode)
        options.append({
            "mode": mode,
            "duration_minutes": plan.get("duration_minutes", 30),
            "distance_km": plan.get("distance_km", 15.0),
            "estimated_cost": plan.get("estimated_cost", 20.0),
            "currency": plan.get("currency", "USD"),
            "summary": plan.get("summary", ""),
            "steps": plan.get("steps", []),
        })

    return {
        "status": "success",
        "origin": origin,
        "destination": destination,
        "city": city,
        "options_count": len(options),
        "options": options,
    }


@router.post("/book", status_code=status.HTTP_201_CREATED)
def book_transport(
    payload: TransportBookRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    """Book a transport option and persist to routes and reservations."""
    trip = db.query(Trip).filter(Trip.id == payload.trip_id).first()
    if not trip:
        raise NotFoundException(message=f"Trip with ID {payload.trip_id} not found", details={"trip_id": payload.trip_id})

    # Plan route details
    plan = routes_provider.plan_route(payload.origin, payload.destination, payload.mode)

    route_record = Route(
        trip_id=trip.id,
        origin=payload.origin,
        destination=payload.destination,
        transport_mode=payload.mode,
        duration_minutes=plan.get("duration_minutes", 30),
        distance_km=plan.get("distance_km", 15.0),
        estimated_cost=payload.cost,
        currency=payload.currency,
        steps_data={"steps": plan.get("steps", []), "notes": payload.notes},
    )
    db.add(route_record)
    db.flush()

    reservation = Reservation(
        trip_id=trip.id,
        user_id=current_user.id if current_user else None,
        reservation_type="transit",
        reference_code=f"TRN-{route_record.id}-{trip.id}",
        provider_name=f"TransportProvider-{payload.mode.title()}",
        status="confirmed",
        total_price=payload.cost,
        currency=payload.currency,
        booking_details={
            "route_id": route_record.id,
            "origin": payload.origin,
            "destination": payload.destination,
            "mode": payload.mode,
        },
    )
    db.add(reservation)
    db.commit()
    db.refresh(reservation)

    return {
        "status": "success",
        "message": f"Transport via {payload.mode} booked successfully",
        "route_id": route_record.id,
        "reservation_id": reservation.id,
        "reference_code": reservation.reference_code,
        "estimated_duration": route_record.duration_minutes,
        "total_price": payload.cost,
    }
