import json
import logging
import re
from .base import Agent
from google import genai
from google.genai import types
from app.core.config import settings
from app.core.gemini_retry import gemini_generate

logger = logging.getLogger("itinerary_agent")


def _clean_json_string(text: str) -> str:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned.strip()


def _build_fallback_days(trip, activities: list) -> list[dict]:
    day_plans = []
    for day_info in activities:
        day = day_info.get("day")
        plan = ", ".join(day_info.get("activities", []))
        if day is not None and plan:
            day_plans.append({"day": day, "plan": plan})
    if not day_plans:
        total_days = getattr(trip, "days", 1) or 1
        destination = getattr(trip, "destination", "Destination")
        style = getattr(trip, "travel_style", "Custom")
        interests = getattr(trip, "interests", "sightseeing")
        for d in range(1, total_days + 1):
            day_plans.append({
                "day": d,
                "plan": f"Explore {destination} highlights focusing on {interests} ({style} style)."
            })
    return day_plans


class ItineraryAgent(Agent):
    """Final itinerary synthesis agent using Gemini LLM."""

    def run(self, context: dict) -> dict:
        trip = context.get("trip")
        if not trip:
            return {"title": "", "summary": "", "data": {"days": []}, "markdown": ""}

        # Gather sub‑agent results (provide empty defaults if missing)
        destination = context.get("destination", {})
        hotel = context.get("hotel", {})
        food = context.get("food", {})
        activity = context.get("activity", {})
        budget = context.get("budget", {})

        # Build a prompt that asks Gemini to synthesize a full itinerary.
        prompt = (
            f"You are a travel planner. Combine the following information into a complete, day‑by‑day travel itinerary.\n"
            f"Trip: {trip.destination}, {trip.days} days, {trip.travelers} travelers, budget {trip.budget}.\n"
            f"Interests: {trip.interests}, travel style: {trip.travel_style}.\n"
            f"\nDestination summary: {destination.get('description', '')}\n"
            f"Destination highlights: {', '.join(destination.get('highlights', []))}\n"
            f"\nHotel summary: {hotel.get('summary', '')}\n"
            f"Hotel recommendations: {json.dumps(hotel.get('recommendations', []))}\n"
            f"\nFood summary: {food.get('summary', '')}\n"
            f"Food recommendations: {json.dumps(food.get('recommendations', []))}\n"
            f"\nBudget: total estimated {budget.get('total_estimated', '')}, details {json.dumps(budget.get('details', {}))}\n"
            f"\nActivities (day_by_day): {json.dumps(activity.get('day_by_day', []))}\n"
            "\nReturn ONLY a JSON object with the following fields:\n"
            "title (string), summary (string), data (object with a 'days' list of {day, plan}), markdown (string).\n"
            "The 'plan' for each day should be a concise description combining activities, suggested meals, and any relevant hotel info.\n"
        )

        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        content = ""
        try:
            response = gemini_generate(
                client=client,
                model=settings.GEMINI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(response_mime_type="application/json"),
            )
            content = response.text.strip()
        except Exception as exc:
            logger.warning("ItineraryAgent Gemini generation call failed: %s. Synthesizing itinerary from sub-agent data.", exc)

        cleaned_content = _clean_json_string(content)
        result = None
        try:
            result = json.loads(cleaned_content)
        except json.JSONDecodeError as exc:
            logger.warning("ItineraryAgent failed to parse JSON: %s. Attempting substring slice. Raw: %r", exc, content)
            start = cleaned_content.find('{')
            end = cleaned_content.rfind('}') + 1
            if start != -1 and end > start:
                try:
                    result = json.loads(cleaned_content[start:end])
                except Exception as inner_exc:
                    logger.warning("ItineraryAgent substring slice failed: %s", inner_exc)

        # Fallback to stub behaviour if JSON parsing failed
        if not result or not isinstance(result, dict):
            logger.warning("ItineraryAgent falling back to stub day-by-day generator due to missing/invalid JSON. Raw: %r", content)
            day_plans = _build_fallback_days(trip, activity.get("day_by_day", []))
            return {
                "title": f"Itinerary for {trip.destination}",
                "summary": destination.get("description") or f"Curated {trip.days}-day itinerary for {trip.destination}.",
                "data": {"days": day_plans},
                "markdown": "\n\n".join([f"### Day {d['day']}\n{d['plan']}" for d in day_plans]),
            }

        # Ensure required keys exist; if not, fall back to stub as above
        required_keys = {"title", "summary", "data", "markdown"}
        if not required_keys.issubset(result.keys()):
            logger.warning("ItineraryAgent missing required keys %s; falling back. Keys found: %s", required_keys - set(result.keys()), list(result.keys()))
            day_plans = _build_fallback_days(trip, activity.get("day_by_day", []))
            return {
                "title": result.get("title") or f"Itinerary for {trip.destination}",
                "summary": result.get("summary") or destination.get("description") or f"Curated {trip.days}-day itinerary for {trip.destination}.",
                "data": result.get("data") if (isinstance(result.get("data"), dict) and "days" in result.get("data", {})) else {"days": day_plans},
                "markdown": result.get("markdown") or "\n\n".join([f"### Day {d['day']}\n{d['plan']}" for d in day_plans]),
            }

        return result
