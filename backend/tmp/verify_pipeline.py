import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.db.session import SessionLocal
from app.db.models.trip import Trip
from app.db.models.itinerary import Itinerary
from app.agents.orchestrator import Orchestrator

def test_full_pipeline():
    db = SessionLocal()
    trip = Trip(
        destination="Rome",
        days=2,
        travelers=2,
        budget=1200,
        interests="history, cuisine",
        travel_style="cultural",
        status="pending",
    )
    db.add(trip)
    db.commit()
    db.refresh(trip)
    trip_id = trip.id
    db.close()

    print(f"Created trip {trip_id} for Rome. Starting orchestrator...")
    start_time = time.time()
    orchestrator = Orchestrator()
    orchestrator.run(trip_id)
    duration = time.time() - start_time
    print(f"Orchestrator completed in {duration:.2f} seconds.")

    db = SessionLocal()
    refreshed_trip = db.query(Trip).filter(Trip.id == trip_id).first()
    itinerary = db.query(Itinerary).filter(Itinerary.trip_id == trip_id).first()

    print("Final Trip Status:", refreshed_trip.status)
    assert refreshed_trip.status == "completed", f"Expected completed, got {refreshed_trip.status}"
    assert itinerary is not None, "Itinerary record was not created!"
    print("Itinerary Title:", itinerary.title)
    print("Itinerary Summary:", itinerary.summary)
    print("Days count in data:", len(itinerary.itinerary_data.get("days", [])))
    print("Days data sample:", itinerary.itinerary_data.get("days", []))
    assert len(itinerary.itinerary_data.get("days", [])) > 0, "Expected non-empty days in itinerary data"
    assert "fallback" not in (itinerary.summary or "").lower(), "Expected real summary, not fallback!"
    print("SUCCESS: End-to-end pipeline succeeded with real AI content!")
    db.close()

if __name__ == "__main__":
    test_full_pipeline()
