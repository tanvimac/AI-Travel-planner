import logging
from app.db.session import engine
from app.db.models import Base
from app.db.schema import init_schema

logger = logging.getLogger("init_db")


def init_db() -> None:
    """Initialize and migrate database tables safely.
    
    Creates Base metadata tables first, then runs schema migrations.
    Fails loudly with an exception if database is unreachable or table creation fails.
    """
    logger.info("Initializing database schema...")
    try:
        # 1. Synchronize SQLAlchemy metadata so core tables (trips, itineraries) exist
        Base.metadata.create_all(bind=engine)
        # 2. Run explicit DDL migrations (ALTER TABLE, indexes, extensions)
        schema_result = init_schema()
        logger.info("Database initialized successfully: %s", schema_result)
    except Exception as exc:
        logger.critical("CRITICAL: Failed to initialize database: %s", exc, exc_info=True)
        raise RuntimeError(f"Database initialization failed: {exc}") from exc


if __name__ == "__main__":
    print("Initializing and verifying database schema...")
    init_db()
    print("Database tables initialized successfully!")
