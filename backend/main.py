from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.router import api_router
from app.db.init_db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize and verify database tables automatically on startup
    init_db()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    lifespan=lifespan,
)

# If wildcard "*" is included in origins, allow_credentials must be False per CORS spec
allow_credentials = "*" not in settings.CORS_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)