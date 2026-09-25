import os
import sys
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.db.session import SessionLocal
from app.db.models.trip import Trip
from app.db.models.itinerary import Itinerary
from app.agents.orchestrator import Orchestrator

def test_isolated_agent_failure():
    db = SessionLocal()
    # Create a test trip
    trip = Trip(
        destination="Tokyo",
        days=3,
        travelers=1,
        budget=1500,
        interests="anime, food",
        travel_style="budget",
        status="pending",
    )
    db.add(trip)
    db.commit()
    db.refresh(trip)
    trip_id = trip.id
    db.close()

    orchestrator = Orchestrator()

    # Mock HotelAgent.run to fail, and ItineraryAgent to succeed with context inspection
    itinerary_received_context = {}

    def mock_itinerary_run(ctx):
        nonlocal itinerary_received_context
        itinerary_received_context = ctx
        return {
            "title": "Itinerary for Tokyo",
            "summary": "Tokyo 3-day exploration",
            "data": {"days": [{"day": 1, "plan": "Explore Akihabara"}]},
            "markdown": "**Day 1**: Explore Akihabara",
        }

    with patch.object(orchestrator.hotel_agent, "run", side_effect=Exception("Simulated Hotel Outage!")), \
         patch.object(orchestrator.destination_agent, "run", return_value={"highlights": ["Tower"], "description": "Tokyo"}), \
         patch.object(orchestrator.food_agent, "run", return_value={"recommendations": [], "summary": "Food"}), \
         patch.object(orchestrator.activity_agent, "run", return_value={"day_by_day": [], "summary": "Activity"}), \
         patch.object(orchestrator.budget_agent, "run", return_value={"total_estimated": 1500, "details": {}}), \
         patch.object(orchestrator.itinerary_agent, "run", side_effect=mock_itinerary_run):
        
        orchestrator.run(trip_id)

    db = SessionLocal()
    refreshed_trip = db.query(Trip).filter(Trip.id == trip_id).first()
    itinerary = db.query(Itinerary).filter(Itinerary.trip_id == trip_id).first()

    print("Trip status:", refreshed_trip.status)
    print("Hotel in context:", itinerary_received_context.get("hotel"))
    print("Itinerary title:", itinerary.title if itinerary else None)

    assert refreshed_trip.status == "completed", f"Expected completed, got {refreshed_trip.status}"
    assert itinerary is not None, "Itinerary was not created!"
    assert itinerary_received_context.get("hotel") == {"recommendations": [], "summary": ""}, "Expected empty default hotel data"
    print("SUCCESS: Trip completed and itinerary saved with empty hotel recommendations despite HotelAgent failure!")
    db.close()

if __name__ == "__main__":
    test_isolated_agent_failure()
