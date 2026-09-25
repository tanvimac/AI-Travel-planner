"""Orchestrator that coordinates travel planning agents."""

import logging
from typing import Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed

from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.db.models.trip import Trip
from app.db.models.itinerary import Itinerary

from app.agents.destination import DestinationAgent
from app.agents.hotel import HotelAgent
from app.agents.food import FoodAgent
from app.agents.activity import ActivityAgent
from app.agents.budget import BudgetAgent
from app.agents.itinerary import ItineraryAgent

logger = logging.getLogger("orchestrator")

DEFAULT_DESTINATION = {"highlights": [], "description": ""}
DEFAULT_HOTEL = {"recommendations": [], "summary": ""}
DEFAULT_FOOD = {"recommendations": [], "summary": ""}
DEFAULT_ACTIVITY = {"day_by_day": [], "summary": ""}
DEFAULT_BUDGET = {"total_estimated": 0, "details": {}}


class Orchestrator:
    """Runs the multi‑agent workflow for a given trip.

    Called as a background task from the ``/plan`` endpoint.
    """

    def __init__(self):
        self.destination_agent = DestinationAgent()
        self.hotel_agent = HotelAgent()
        self.food_agent = FoodAgent()
        self.activity_agent = ActivityAgent()
        self.budget_agent = BudgetAgent()
        self.itinerary_agent = ItineraryAgent()

    def run(self, trip_id: int) -> None:
        """Entry point for FastAPI ``BackgroundTasks``.

        Args:
            trip_id: Primary key of the ``Trip`` row that was created by the API call.
        """
        db: Session = SessionLocal()
        try:
            # Load the trip record
            trip: Trip = db.query(Trip).filter(Trip.id == trip_id).first()
            if not trip:
                logger.error("Trip %s not found", trip_id)
                return

            # Build context passed between agents
            context: Dict[str, Any] = {
                "trip": trip,
            }

            # Helper to run an agent safely with isolated exception handling
            def execute_agent(agent_name: str, agent, default_val: Any) -> tuple[str, Any]:
                try:
                    logger.info("Starting %s for trip %s", agent_name, trip_id)
                    res = agent.run(context)
                    logger.info("Completed %s for trip %s", agent_name, trip_id)
                    return agent_name, res
                except Exception as exc:
                    logger.exception(
                        "Agent %s failed for trip %s: %s. Using default fallback.",
                        agent_name,
                        trip_id,
                        exc,
                    )
                    return agent_name, default_val

            # Run independent agents in parallel (Tasks 7 & 8)
            parallel_agents = [
                ("destination", self.destination_agent, DEFAULT_DESTINATION),
                ("hotel", self.hotel_agent, DEFAULT_HOTEL),
                ("food", self.food_agent, DEFAULT_FOOD),
                ("activity", self.activity_agent, DEFAULT_ACTIVITY),
                ("budget", self.budget_agent, DEFAULT_BUDGET),
            ]

            with ThreadPoolExecutor(max_workers=len(parallel_agents)) as executor:
                futures = [
                    executor.submit(execute_agent, name, agent, default)
                    for name, agent, default in parallel_agents
                ]
                for future in as_completed(futures):
                    key, val = future.result()
                    context[key] = val

            # Run the synthesis ItineraryAgent (only mark failed if this step itself fails)
            logger.info("Running ItineraryAgent for trip %s", trip_id)
            try:
                itinerary_result = self.itinerary_agent.run(context)
            except Exception as exc:
                logger.exception("ItineraryAgent failed for trip %s: %s", trip_id, exc)
                raise

            # Persist the itinerary
            itinerary = Itinerary(
                trip_id=trip.id,
                title=itinerary_result.get("title"),
                summary=itinerary_result.get("summary"),
                itinerary_data=itinerary_result.get("data", {}),
                raw_markdown=itinerary_result.get("markdown"),
            )
            db.add(itinerary)
            # Update trip status
            trip.status = "completed"
            db.commit()
            logger.info("Itinerary stored and trip %s marked completed", trip_id)
        except Exception as e:
            logger.exception("Orchestrator failed for trip %s: %s", trip_id, e)
            try:
                db.rollback()
                trip = db.query(Trip).filter(Trip.id == trip_id).first()
                if trip:
                    trip.status = "failed"
                    db.commit()
            except Exception:
                db.rollback()
        finally:
            db.close()
