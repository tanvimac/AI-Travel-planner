from .base import Agent
from google import genai
from app.core.config import settings
from app.core.gemini_retry import gemini_generate

class ActivityAgent(Agent):
    """Activity recommendation agent using Gemini LLM."""

    def run(self, context: dict) -> dict:
        trip = context.get('trip')
        if not trip:
            return {"day_by_day": [], "summary": ""}
        # Initialise Gemini client
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        # Build a prompt that asks for a brief summary and day‑by‑day activities.
        prompt = (
            f"You are a travel planner. Provide a short summary for the trip and a day‑by‑day list of activities.\n"
            f"Destination: {trip.destination}\n"
            f"Days: {trip.days}\n"
            f"Travelers: {trip.travelers}\n"
            f"Budget: {trip.budget}\n"
            f"Interests: {trip.interests}\n"
            f"Travel style: {trip.travel_style}\n"
            "Return the first line as a summary. Then for each day output a line in the format: Day X: activity1, activity2, ..."
        )
        response = gemini_generate(
            client=client,
            model=settings.GEMINI_MODEL,
            contents=prompt,
        )
        content = response.text.strip()
        lines = [line.strip() for line in content.splitlines() if line.strip()]
        summary = lines[0] if lines else ""
        day_by_day = []
        for line in lines[1:]:
            # Expect format "Day X: activity1, activity2"
            if ":" in line:
                day_part, activities_part = line.split(":", 1)
                # Extract day number
                try:
                    day_num = int(day_part.strip().replace("Day", "").strip())
                except ValueError:
                    continue
                activities = [act.strip() for act in activities_part.split(",") if act.strip()]
                day_by_day.append({"day": day_num, "activities": activities})
        return {"day_by_day": day_by_day, "summary": summary}
