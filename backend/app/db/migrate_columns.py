from sqlalchemy import text
from app.db.session import engine

def migrate():
    with engine.begin() as conn:
        conn.execute(text("ALTER TABLE trips ADD COLUMN IF NOT EXISTS user_id INTEGER REFERENCES users(id) ON DELETE SET NULL;"))
        conn.execute(text("ALTER TABLE trips ADD COLUMN IF NOT EXISTS title VARCHAR(255);"))
        conn.execute(text("ALTER TABLE trips ADD COLUMN IF NOT EXISTS currency VARCHAR(10) DEFAULT 'USD';"))
        conn.execute(text("ALTER TABLE trips ADD COLUMN IF NOT EXISTS start_date DATE;"))
        conn.execute(text("ALTER TABLE trips ADD COLUMN IF NOT EXISTS end_date DATE;"))
    print("Trips columns migrated successfully!")

if __name__ == "__main__":
    migrate()
