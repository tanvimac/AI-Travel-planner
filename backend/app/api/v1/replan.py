import logging
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.deps import get_optional_current_user
from app.db.models.user import User
from app.db.models.trip import Trip, TripEvent
from app.schemas.v1_schemas import ReplanRequest
from app.services.planner_service import PlannerService
from app.core.errors import NotFoundException, ValidationException

logger = logging.getLogger("replan_api")
router = APIRouter(prefix="/replan", tags=["Dynamic Replanner"])


@router.post("/", status_code=status.HTTP_200_OK)
def replan_trip(
    payload: ReplanRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    """Dynamically adjust an existing trip and regenerate itinerary without losing context."""
    trip = db.query(Trip).filter(Trip.id == payload.trip_id).first()
    if not trip:
        raise NotFoundException(message=f"Trip with ID {payload.trip_id} not found", details={"trip_id": payload.trip_id})

    ctype = payload.change_type.lower()
    old_value = None

    if ctype == "budget":
        try:
            val = float(payload.new_value)
            if val < 50.0:
                raise ValueError()
            old_value = trip.budget
            trip.budget = val
        except (ValueError, TypeError):
            raise ValidationException("New budget value must be a valid number >= 50.0")

    elif ctype in ["days", "duration"]:
        try:
            val = int(payload.new_value)
            if val < 1 or val > 30:
                raise ValueError()
            old_value = trip.days
            trip.days = val
        except (ValueError, TypeError):
            raise ValidationException("Duration must be an integer between 1 and 30 days")

    elif ctype in ["interests", "theme"]:
        old_value = trip.interests
        trip.interests = str(payload.new_value)

    elif ctype in ["travel_style", "style"]:
        old_value = trip.travel_style
        trip.travel_style = str(payload.new_value)

    elif ctype in ["travelers", "group_size"]:
        try:
            val = int(payload.new_value)
            if val < 1:
                raise ValueError()
            old_value = trip.travelers
            trip.travelers = val
        except (ValueError, TypeError):
            raise ValidationException("Travelers must be a positive integer")
    else:
        raise ValidationException(
            f"Unsupported change_type '{payload.change_type}'. Supported: budget, days, interests, travel_style, travelers"
        )

    # Log audit event
    event = TripEvent(
        trip_id=trip.id,
        event_type="replanned",
        message=f"Trip replanned: {ctype} modified from '{old_value}' to '{payload.new_value}'",
        event_data={
            "change_type": ctype,
            "old_value": old_value,
            "new_value": payload.new_value,
            "reason": payload.reason or "User triggered replan",
        },
    )
    db.add(event)
    trip.status = "pending"
    db.commit()

    # Regenerate plan synchronously to have updated itinerary immediately ready
    planner = PlannerService(db)
    updated_plan = planner.generate_plan_sync(trip.id)

    db.refresh(trip)

    return {
        "status": "success",
        "message": f"Trip {trip.id} successfully replanned and refreshed",
        "change_type": ctype,
        "old_value": old_value,
        "new_value": payload.new_value,
        "trip": {
            "id": trip.id,
            "destination": trip.destination,
            "days": trip.days,
            "budget": trip.budget,
            "travel_style": trip.travel_style,
            "interests": trip.interests,
            "status": trip.status,
        },
        "event_id": event.id,
        "itinerary": updated_plan.get("itinerary") if updated_plan else None,
    }


@router.get("/history/{trip_id}")
def get_replan_history(
    trip_id: int = Path(..., description="ID of the trip"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    """Retrieve history of replanning modifications and events for a trip."""
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise NotFoundException(message=f"Trip with ID {trip_id} not found", details={"trip_id": trip_id})

    events = (
        db.query(TripEvent)
        .filter(TripEvent.trip_id == trip_id)
        .order_by(TripEvent.created_at.desc())
        .all()
    )

    return {
        "status": "success",
        "trip_id": trip_id,
        "events_count": len(events),
        "history": [
            {
                "id": ev.id,
                "event_type": ev.event_type,
                "message": ev.message,
                "data": ev.event_data,
                "timestamp": ev.created_at.isoformat() if ev.created_at else None,
            }
            for ev in events
        ],
    }
