import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from unittest.mock import patch
from app.db.init_db import init_db

# Patch engine to raise OperationalError on connect/create_all
with patch("app.db.init_db.Base.metadata.create_all", side_effect=Exception("Database unreachable on port 9999")):
    try:
        init_db()
        print("FAILED: init_db did not raise!")
        sys.exit(1)
    except RuntimeError as exc:
        print("SUCCESS: init_db failed loudly with RuntimeError as expected:", exc)
