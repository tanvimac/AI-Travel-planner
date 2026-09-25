from fastapi import APIRouter
from app.api.v1 import health, planner

api_router = APIRouter()

# Root & health endpoints (unprefixed)
api_router.include_router(health.root_router)

# API v1 routes (consistent /api prefix)
api_router.include_router(health.test_router, prefix="/api")
api_router.include_router(planner.router, prefix="/api")
