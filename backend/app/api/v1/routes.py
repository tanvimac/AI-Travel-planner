from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.travel import Route
from app.schemas.v1_schemas import RouteRequest
from app.providers.routes import RouteProvider

router = APIRouter(prefix="/routes", tags=["Routes & Directions"])
provider = RouteProvider()


@router.post("/plan")
def plan_route(request: RouteRequest, db: Session = Depends(get_db)):
    """Calculate navigational route, distance, duration, and transit steps."""
    result = provider.plan_route(
        origin=request.origin,
        destination=request.destination,
        mode=request.mode,
    )

    # Persist in routes table
    route = Route(
        origin=result["origin"],
        destination=result["destination"],
        transport_mode=result["transport_mode"],
        duration_minutes=result["duration_minutes"],
        distance_km=result["distance_km"],
        estimated_cost=result["estimated_cost"],
        currency=result["currency"],
        steps_data={"steps": result["steps"]},
    )
    db.add(route)
    db.commit()
    db.refresh(route)

    return {
        "id": route.id,
        **result,
        "created_at": route.created_at.isoformat(),
    }


@router.get("/history")
def get_routes_history(limit: int = 20, db: Session = Depends(get_db)):
    """Retrieve recent calculated transit and navigation routes."""
    routes = db.query(Route).order_by(Route.id.desc()).limit(limit).all()
    return [
        {
            "id": r.id,
            "origin": r.origin,
            "destination": r.destination,
            "transport_mode": r.transport_mode,
            "duration_minutes": r.duration_minutes,
            "distance_km": r.distance_km,
            "estimated_cost": r.estimated_cost,
            "currency": r.currency,
            "steps": r.steps_data.get("steps", []) if r.steps_data else [],
            "created_at": r.created_at.isoformat(),
        }
        for r in routes
    ]
