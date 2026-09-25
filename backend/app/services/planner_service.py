from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.schemas.planner import TravelRequest
from app.db.models.trip import Trip
from app.agents.orchestrator import Orchestrator


def create_travel_plan(request: TravelRequest, db: Session) -> dict:
    try:
        trip = Trip(
            destination=request.destination,
            days=request.days,
            travelers=request.travelers,
            budget=request.budget,
            interests=request.interests,
            travel_style=request.travelStyle or "Mid-range",
            status="pending",
        )
        db.add(trip)
        db.commit()
        db.refresh(trip)

        return {
            "message": "Travel request received successfully!",
            "id": trip.id,
            "destination": trip.destination,
            "days": trip.days,
            "travelers": trip.travelers,
            "budget": trip.budget,
            "interests": trip.interests,
            "travelStyle": trip.travel_style,
            "status": trip.status,
            "created_at": trip.created_at.isoformat() if trip.created_at else None,
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to save travel plan: {str(e)}")


def get_all_trips(db: Session) -> list[dict]:
    try:
        trips = db.query(Trip).order_by(Trip.id.desc()).all()
        return [
            {
                "id": t.id,
                "destination": t.destination,
                "days": t.days,
                "travelers": t.travelers,
                "budget": t.budget,
                "interests": t.interests,
                "travelStyle": t.travel_style,
                "status": t.status,
                "created_at": t.created_at.isoformat() if t.created_at else None,
            }
            for t in trips
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch trips: {str(e)}")


def get_trip_by_id(trip_id: int, db: Session) -> dict:
    try:
        trip = db.query(Trip).filter(Trip.id == trip_id).first()

        if not trip:
            raise HTTPException(
                status_code=404,
                detail=f"Trip with id {trip_id} not found"
            )

        itinerary = trip.itineraries[-1] if trip.itineraries else None

        return {
            "id": trip.id,
            "destination": trip.destination,
            "days": trip.days,
            "travelers": trip.travelers,
            "budget": trip.budget,
            "interests": trip.interests,
            "travelStyle": trip.travel_style,
            "status": trip.status,
            "created_at": trip.created_at.isoformat() if trip.created_at else None,
            "itinerary": {
                "id": itinerary.id,
                "title": itinerary.title,
                "summary": itinerary.summary,
                "data": itinerary.itinerary_data,
                "markdown": itinerary.raw_markdown,
                "created_at": (
                    itinerary.created_at.isoformat()
                    if itinerary.created_at
                    else None
                ),
            } if itinerary else None,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch trip: {str(e)}"
        )


class PlannerService:
    """Service layer class for trip planning and multi-agent AI orchestration."""

    def __init__(self, db: Session):
        self.db = db

    def create_plan(self, request: TravelRequest) -> dict:
        return create_travel_plan(request, self.db)

    def get_trips(self) -> list[dict]:
        return get_all_trips(self.db)

    def get_trip(self, trip_id: int) -> dict:
        return get_trip_by_id(trip_id, self.db)

    def generate_plan_sync(self, trip_id: int) -> dict:
        orchestrator = Orchestrator()
        orchestrator.run(trip_id)
        return get_trip_by_id(trip_id, self.db)
