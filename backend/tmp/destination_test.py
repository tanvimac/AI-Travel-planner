import os
import sys

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.agents.destination import DestinationAgent
from app.db.models.trip import Trip

# Create a dummy Trip instance matching the ORM fields
trip = Trip(
    destination="Paris",
    days=5,
    travelers=2,
    budget=2000,
    interests="art, food",
    travel_style="mid-range",
)

context = {"trip": trip}

agent = DestinationAgent()
result = agent.run(context)
print(result)
