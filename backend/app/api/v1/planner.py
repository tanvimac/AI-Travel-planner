from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session
from app.schemas.planner import TravelRequest
from app.services.planner_service import create_travel_plan, get_all_trips, get_trip_by_id
from app.db.session import get_db
from app.agents.orchestrator import Orchestrator

router = APIRouter()

@router.post("/plan")
def plan_trip(
    request: TravelRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """Create a trip entry and start the orchestration in background.
    Returns immediate response with trip id and pending status.
    """
    result = create_travel_plan(request, db)
    trip_id = result["id"]
    # Schedule orchestrator to run after response
    background_tasks.add_task(Orchestrator().run, trip_id)
    return {"id": trip_id, "status": "pending"}

@router.get("/trips")
def get_trips(db: Session = Depends(get_db)):
    return get_all_trips(db)

@router.get("/trips/{trip_id}")
def get_trip(trip_id: int, db: Session = Depends(get_db)):
    return get_trip_by_id(trip_id, db)
