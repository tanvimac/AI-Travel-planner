from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date
from app.db.session import get_db
from app.db.models.environment import WeatherSnapshot
from app.providers.weather import WeatherProvider

router = APIRouter(prefix="/weather", tags=["Weather"])
provider = WeatherProvider()


@router.get("")
@router.get("/")
def get_weather(
    city: str = Query(..., min_length=2, description="Target city for weather forecast"),
    days: int = Query(default=5, ge=1, le=7),
    db: Session = Depends(get_db),
):
    """Retrieve live meteorological conditions and multi-day forecast for a city."""
    data = provider.get_weather_for_city(city=city, days=days)

    # Cache weather snapshot in database
    current = data.get("current", {})
    snapshot = WeatherSnapshot(
        city=city,
        country=data.get("country", ""),
        snapshot_date=date.today(),
        temperature_celsius=current.get("temperature_c", 20.0),
        feels_like_celsius=current.get("feels_like_c"),
        condition=current.get("condition", "Pleasant"),
        humidity_percent=current.get("humidity_percent"),
        wind_speed_kmh=current.get("wind_speed_kmh"),
        forecast_json={"forecast": data.get("forecast", [])},
    )
    try:
        db.add(snapshot)
        db.commit()
    except Exception:
        db.rollback()

    return {
        "status": "success",
        "weather": data,
        **data,
    }
