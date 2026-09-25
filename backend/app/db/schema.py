"""
Database Schema Initialization and Migration Module.
Reuses get_db_connection() from app.db.connection to apply schema changes safely
without modifying or resetting existing data.
"""

from app.db.connection import get_db_connection


CREATE_SCHEMA_SQL = """
-- 1. Ensure extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 2. Safely add missing columns to existing trips table
ALTER TABLE trips 
ADD COLUMN IF NOT EXISTS status VARCHAR(50) NOT NULL DEFAULT 'pending';

ALTER TABLE trips 
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE trips 
ADD COLUMN IF NOT EXISTS user_id INTEGER REFERENCES users(id) ON DELETE SET NULL;

ALTER TABLE trips 
ADD COLUMN IF NOT EXISTS title VARCHAR(255);

ALTER TABLE trips 
ADD COLUMN IF NOT EXISTS currency VARCHAR(10) NOT NULL DEFAULT 'USD';

ALTER TABLE trips 
ADD COLUMN IF NOT EXISTS start_date DATE;

ALTER TABLE trips 
ADD COLUMN IF NOT EXISTS end_date DATE;


-- 3. Create itineraries table for AI-generated trip plans
CREATE TABLE IF NOT EXISTS itineraries (
    id SERIAL PRIMARY KEY,
    trip_id INTEGER NOT NULL REFERENCES trips(id) ON DELETE CASCADE,
    title VARCHAR(255),
    summary TEXT,
    itinerary_data JSONB NOT NULL DEFAULT '{}'::jsonb,
    raw_markdown TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 4. Create index on foreign key for fast lookups
CREATE INDEX IF NOT EXISTS idx_itineraries_trip_id ON itineraries(trip_id);
"""


def init_schema() -> dict:
    """
    Executes schema creation and non-destructive column migrations.
    Returns status and summary of verified tables.
    """
    conn = None
    try:
        conn = get_db_connection()
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(CREATE_SCHEMA_SQL)

            # Query existing tables and column counts to confirm
            cur.execute("""
                SELECT table_name, count(column_name) 
                FROM information_schema.columns 
                WHERE table_name IN ('trips', 'itineraries')
                GROUP BY table_name;
            """)
            tables = dict(cur.fetchall())

        return {
            "status": "success",
            "message": "Database schema verified and up-to-date",
            "tables": tables,
        }
    finally:
        if conn and not conn.closed:
            conn.close()


if __name__ == "__main__":
    print("Applying database schema...")
    result = init_schema()
    print("Result:", result)
