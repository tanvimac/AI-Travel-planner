import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.db.connection import get_db_connection

conn = get_db_connection()
cur = conn.cursor()
cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
tables = [r[0] for r in cur.fetchall()]
print("Tables in public schema:", tables)
assert "trips" in tables, "trips table missing!"
assert "itineraries" in tables, "itineraries table missing!"
print("SUCCESS: trips and itineraries tables verified!")
conn.close()
