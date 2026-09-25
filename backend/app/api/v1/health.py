from fastapi import APIRouter, HTTPException, status
import psycopg2
from app.db.connection import test_connection

# Root & health endpoints (mounted without prefix at root: /, /health)
root_router = APIRouter()

# Diagnostic & test endpoints (mounted with /api prefix in router.py: /api/test, /api/db-test)
test_router = APIRouter()

# Backward compatibility alias
router = root_router


@root_router.get("/")
def home():
    return {
        "message": "AI Travel Planner API is running!"
    }


@root_router.get("/health")
def health():
    return {
        "status": "healthy"
    }


@test_router.get("/test")
def test_api():
    return {
        "message": "Hello from FastAPI!",
        "status": "success"
    }


@test_router.get("/db-test")
def test_db():
    try:
        db_info = test_connection()
        return {
            "status": "success",
            "message": "PostgreSQL database connected successfully!",
            "database": db_info,
        }
    except psycopg2.OperationalError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": "error",
                "message": "Failed to connect to PostgreSQL database",
                "error": str(e).strip(),
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "error",
                "message": "An unexpected error occurred while testing database connection",
                "error": str(e).strip(),
            },
        )
