from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.schemas.planner import TravelRequest
from app.db.models import Trip


def create_travel_plan(request: TravelRequest, db: Session) -> dict:
    try:
        trip = Trip(
            destination=request.destination,
            days=request.days,
            travelers=request.travelers,
            budget=request.budget,
            interests=request.interests,
            travel_style=request.travelStyle or "Mid-range",
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
    
