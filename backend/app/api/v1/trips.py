from typing import Optional, List, Dict, Any
from fastapi import APIRouter, BackgroundTasks, Depends, Path, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.db.session import get_db
from app.db.models.trip import Trip, Traveler
from app.db.models.user import User
from app.schemas.v1_schemas import TripCreateV1Request
from app.schemas.planner import TravelRequest
from app.services.planner_service import get_all_trips, get_trip_by_id
from app.agents.orchestrator import Orchestrator
from app.core.deps import get_optional_current_user
from app.core.errors import NotFoundException

router = APIRouter(prefix="/trips", tags=["Trips"])


class TravelerAddRequest(BaseModel):
    name: str = Field(..., min_length=1)
    email: Optional[str] = None
    role: str = "traveler"
    dietary_preferences: Optional[str] = None
    notes: Optional[str] = None


@router.post("", status_code=status.HTTP_201_CREATED)
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_trip(
    request: TripCreateV1Request,
    background_tasks: BackgroundTasks,
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db),
):
    """
    Submit a travel planning request.
    Inserts trip into database with 'pending' status and launches AI Orchestrator in background.
    """
    trip = Trip(
        user_id=current_user.id if current_user else None,
        destination=request.destination,
        days=request.days,
        travelers=request.travelers,
        budget=request.budget,
        currency=request.currency or "USD",
        interests=request.interests,
        travel_style=request.travel_style or "Mid-range",
        status="pending",
    )
    db.add(trip)
    db.commit()
    db.refresh(trip)

    # Launch background agent orchestration
    background_tasks.add_task(Orchestrator().run, trip.id)

    trip_info = {
        "id": trip.id,
        "destination": trip.destination,
        "days": trip.days,
        "travelers": trip.travelers,
        "budget": trip.budget,
        "currency": trip.currency,
        "status": trip.status,
        "created_at": trip.created_at.isoformat(),
    }

    return {
        **trip_info,
        "trip": trip_info,
        "message": "Trip created. AI agents are currently curating your itinerary in background.",
    }


@router.post("/plan", status_code=status.HTTP_201_CREATED)
def plan_trip_v1(
    request: TravelRequest,
    background_tasks: BackgroundTasks,
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db),
):
    """Compatible alias endpoint for /api/v1/trips/plan."""
    trip = Trip(
        user_id=current_user.id if current_user else None,
        destination=request.destination,
        days=request.days,
        travelers=request.travelers,
        budget=request.budget,
        currency="USD",
        interests=request.interests,
        travel_style=request.travelStyle or "Mid-range",
        status="pending",
    )
    db.add(trip)
    db.commit()
    db.refresh(trip)

    background_tasks.add_task(Orchestrator().run, trip.id)
    return {"id": trip.id, "status": "pending"}


@router.get("")
@router.get("/")
def list_trips(
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db),
):
    """List all trips in reverse chronological order."""
    query = db.query(Trip)
    if current_user:
        query = query.filter(Trip.user_id == current_user.id)

    trips = query.order_by(Trip.id.desc()).all()
    trips_list = [
        {
            "id": t.id,
            "destination": t.destination,
            "days": t.days,
            "travelers": t.travelers,
            "budget": t.budget,
            "currency": t.currency,
            "interests": t.interests,
            "travelStyle": t.travel_style,
            "status": t.status,
            "created_at": t.created_at.isoformat() if t.created_at else None,
        }
        for t in trips
    ]
    return {
        "status": "success",
        "count": len(trips_list),
        "trips": trips_list,
    }


@router.get("/{trip_id}")
def get_trip(
    trip_id: int = Path(..., description="ID of the trip"),
    db: Session = Depends(get_db),
):
    """Fetch complete trip status, metadata, and generated itinerary."""
    data = get_trip_by_id(trip_id, db)
    return {
        "status": "success",
        "trip": data,
        **data,
    }


@router.delete("/{trip_id}")
def delete_trip(
    trip_id: int = Path(..., description="ID of the trip"),
    db: Session = Depends(get_db),
):
    """Delete a trip and cascade delete all associated itineraries and reservations."""
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise NotFoundException(resource="Trip", identifier=trip_id)

    db.delete(trip)
    db.commit()
    return {"status": "success", "message": f"Trip {trip_id} deleted successfully"}


@router.get("/{trip_id}/travelers")
def list_travelers(
    trip_id: int = Path(..., description="ID of the trip"),
    db: Session = Depends(get_db),
):
    """List travelers registered for a specific trip."""
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise NotFoundException(resource="Trip", identifier=trip_id)

    return {
        "status": "success",
        "trip_id": trip_id,
        "travelers": [
            {
                "id": tr.id,
                "name": tr.name,
                "email": tr.email,
                "role": tr.role,
                "dietary_preferences": tr.dietary_preferences,
                "notes": tr.notes,
            }
            for tr in trip.travelers_list
        ],
    }


@router.post("/{trip_id}/travelers", status_code=status.HTTP_201_CREATED)
def add_traveler(
    payload: TravelerAddRequest,
    trip_id: int = Path(..., description="ID of the trip"),
    db: Session = Depends(get_db),
):
    """Add a traveler to an existing trip."""
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise NotFoundException(resource="Trip", identifier=trip_id)

    traveler = Traveler(
        trip_id=trip.id,
        name=payload.name,
        email=payload.email,
        role=payload.role,
        dietary_preferences=payload.dietary_preferences,
        notes=payload.notes,
    )
    db.add(traveler)
    db.commit()
    db.refresh(traveler)

    return {
        "status": "success",
        "traveler_id": traveler.id,
        "name": traveler.name,
        "role": traveler.role,
    }
