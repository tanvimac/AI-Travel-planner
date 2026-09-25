from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from app.db.session import get_db
from app.db.models.travel import Place, SavedPlace
from app.db.models.user import User
from app.providers.places import PlacesProvider
from app.core.deps import get_optional_current_user

router = APIRouter(prefix="/places", tags=["Places & POI"])
provider = PlacesProvider()


class SavePlaceRequest(BaseModel):
    name: str = Field(..., min_length=1)
    notes: Optional[str] = None
    trip_id: Optional[int] = None


@router.get("/search")
def search_places(
    query: str = Query(..., min_length=1),
    city: Optional[str] = None,
    limit: int = Query(default=5, ge=1, le=20),
):
    """Search points of interest, architectural landmarks, and attractions."""
    results = provider.search_places(query=query, city=city, limit=limit)
    return {
        "query": query,
        "city": city,
        "count": len(results),
        "places": results,
    }


@router.post("/saved", status_code=status.HTTP_201_CREATED)
def save_place(
    payload: SavePlaceRequest,
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db),
):
    """Save a place or bookmark to favorites or a specific trip."""
    saved = SavedPlace(
        name=payload.name,
        notes=payload.notes,
        trip_id=payload.trip_id,
        user_id=current_user.id if current_user else None,
    )
    db.add(saved)
    db.commit()
    db.refresh(saved)
    return {
        "status": "success",
        "id": saved.id,
        "name": saved.name,
        "notes": saved.notes,
        "trip_id": saved.trip_id,
        "created_at": saved.created_at.isoformat(),
    }


@router.get("/saved")
def get_saved_places(
    trip_id: Optional[int] = Query(None, description="Filter by trip ID"),
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db),
):
    """List saved places."""
    query = db.query(SavedPlace)
    if trip_id is not None:
        query = query.filter(SavedPlace.trip_id == trip_id)
    elif current_user:
        query = query.filter(SavedPlace.user_id == current_user.id)

    items = query.order_by(SavedPlace.id.desc()).all()
    saved_list = [
        {
            "id": p.id,
            "name": p.name,
            "notes": p.notes,
            "trip_id": p.trip_id,
            "created_at": p.created_at.isoformat(),
        }
        for p in items
    ]
    return {
        "status": "success",
        "count": len(saved_list),
        "saved_places": saved_list,
    }
