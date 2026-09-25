import logging
from datetime import datetime, timezone
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, status
import psycopg2
from app.db.connection import test_connection
from app.providers.weather import WeatherProvider
from app.providers.currency import CurrencyProvider
from app.providers.places import PlacesProvider
from app.providers.flights import FlightProvider
from app.providers.hotels import HotelProvider
from app.providers.restaurants import RestaurantProvider
from app.providers.routes import RoutesProvider
from app.core.config import settings

logger = logging.getLogger("health_api")

# Root & health endpoints (mounted without prefix at root: /, /health, /health/providers)
root_router = APIRouter()

# Diagnostic & test endpoints (mounted with /api prefix in router.py: /api/test, /api/db-test)
test_router = APIRouter()

# Backward compatibility alias
router = root_router

# Provider singletons for health checks
_weather_provider = WeatherProvider()
_currency_provider = CurrencyProvider()
_places_provider = PlacesProvider()
_flight_provider = FlightProvider()
_hotel_provider = HotelProvider()
_restaurant_provider = RestaurantProvider()
_routes_provider = RoutesProvider()


@root_router.get("/")
def home():
    return {
        "message": "AI Travel Planner API is running!",
        "version": "2.0.0",
        "docs": "/docs",
    }


@root_router.get("/health")
def health():
    """Overall system health status."""
    db_status = "connected"
    try:
        test_connection()
    except Exception as e:
        logger.error("DB health check error: %s", e)
        db_status = "unavailable"

    is_healthy = db_status == "connected"
    return {
        "status": "healthy" if is_healthy else "degraded",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "database": db_status,
        "version": "2.0.0",
    }


@root_router.get("/health/providers")
def health_providers() -> Dict[str, Any]:
    """
    Check the operational status of all third-party and internal travel providers.
    Safe and sanitized: Never exposes API keys, tokens, or connection strings.
    """
    results: Dict[str, Any] = {}

    # 1. Weather Provider
    try:
        results["weather"] = _weather_provider.check_health()
    except Exception as e:
        results["weather"] = {"provider": "weather", "status": "unhealthy", "error": "Provider check failed"}

    # 2. Currency Provider
    try:
        results["currency"] = _currency_provider.check_health()
    except Exception as e:
        results["currency"] = {"provider": "currency", "status": "unhealthy", "error": "Provider check failed"}

    # 3. Places Provider
    try:
        results["places"] = _places_provider.check_health()
    except Exception as e:
        results["places"] = {"provider": "places", "status": "unhealthy", "error": "Provider check failed"}

    # 4. Flight Provider
    try:
        results["flights"] = _flight_provider.check_health()
    except Exception as e:
        results["flights"] = {"provider": "flights", "status": "unhealthy", "error": "Provider check failed"}

    # 5. Lodging / Hotel Provider
    try:
        results["hotels"] = _hotel_provider.check_health()
    except Exception as e:
        results["hotels"] = {"provider": "hotels", "status": "unhealthy", "error": "Provider check failed"}

    # 6. Restaurant Provider
    try:
        results["restaurants"] = _restaurant_provider.check_health()
    except Exception as e:
        results["restaurants"] = {"provider": "restaurants", "status": "unhealthy", "error": "Provider check failed"}

    # 7. Transit / Route Provider
    try:
        results["routes"] = _routes_provider.check_health()
    except Exception as e:
        results["routes"] = {"provider": "routes", "status": "unhealthy", "error": "Provider check failed"}

    # 8. AI Orchestrator
    ai_status = "healthy" if bool(settings.GEMINI_API_KEY) else "fallback_only"
    results["ai_orchestrator"] = {
        "provider": "google-gemini",
        "model": settings.GEMINI_MODEL,
        "status": ai_status,
    }

    # Aggregate status: healthy if all essential providers are healthy or degraded
    all_ok = all(
        p.get("status") in ["healthy", "degraded", "fallback_only"]
        for p in results.values()
    )

    return {
        "status": "healthy" if all_ok else "degraded",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "providers": results,
    }


@test_router.get("/test")
def test_api():
    return {
        "message": "Hello from FastAPI!",
        "status": "success",
    }


@test_router.get("/db-test")
def test_db():
    try:
        db_info = test_connection()
        return {
            "status": "success",
            "message": "PostgreSQL database connected successfully!",
            "database": {
                "status": db_info.get("status"),
                "database": db_info.get("database"),
                "version": db_info.get("version"),
            },
        }
    except psycopg2.OperationalError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": "error",
                "message": "Failed to connect to PostgreSQL database",
                "error": "Connection error",
            },
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "error",
                "message": "An unexpected error occurred while testing database connection",
            },
        )
