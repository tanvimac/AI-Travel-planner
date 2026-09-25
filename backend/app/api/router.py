from fastapi import APIRouter
from app.api.v1 import (
    health,
    planner,
    auth,
    trips,
    routes,
    places,
    weather,
    currency,
    flights,
    hotels,
    restaurants,
    transport,
    budget,
    concierge,
    replan,
)

api_router = APIRouter()

# 1. Root & Health Endpoints (unprefixed: /, /health, /health/providers)
api_router.include_router(health.root_router)

# 2. Diagnostic endpoints
api_router.include_router(health.test_router, prefix="/api")

# 3. Existing Legacy / Frontend Backward Compatible Endpoints (/api/plan, /api/trips)
api_router.include_router(planner.router, prefix="/api")

# 4. Phase 2 Target Architecture: /api/v1/* Endpoints
v1_router = APIRouter(prefix="/api/v1")
v1_router.include_router(auth.router)
v1_router.include_router(trips.router)
v1_router.include_router(routes.router)
v1_router.include_router(places.router)
v1_router.include_router(weather.router)
v1_router.include_router(currency.router)
v1_router.include_router(flights.router)
v1_router.include_router(hotels.router)
v1_router.include_router(restaurants.router)
v1_router.include_router(transport.router)
v1_router.include_router(budget.router)
v1_router.include_router(concierge.router)
v1_router.include_router(replan.router)

api_router.include_router(v1_router)
