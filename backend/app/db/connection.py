import psycopg2
from app.core.config import settings


def get_db_connection():
    """
    Establish and return a new PostgreSQL connection using psycopg2.
    Connection parameters are read from environment variables via application settings.
    """
    return psycopg2.connect(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        dbname=settings.DB_NAME,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        connect_timeout=5,
    )


def test_connection() -> dict:
    """
    Tests the PostgreSQL connection by querying server version, current database, and user.
    Safely closes the connection before returning.
    """
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            version_row = cur.fetchone()
            version = version_row[0] if version_row else "Unknown"

            cur.execute("SELECT current_database(), current_user;")
            db_row = cur.fetchone()
            current_db, current_user = db_row if db_row else ("Unknown", "Unknown")

        return {
            "status": "connected",
            "database": current_db,
            "user": current_user,
            "version": version,
        }
    finally:
        if conn and not conn.closed:
            conn.close()
