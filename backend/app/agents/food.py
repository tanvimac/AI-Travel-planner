from .base import Agent
from google import genai
from app.core.config import settings
from app.core.gemini_retry import gemini_generate

class FoodAgent(Agent):
    """Food recommendation agent using Gemini LLM."""

    def run(self, context: dict) -> dict:
        trip = context.get('trip')
        if not trip:
            return {"recommendations": [], "summary": ""}
        # Initialise Gemini client
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        # Build a prompt with trip details
        prompt = (
            f"You are a travel planner. Provide a brief food recommendation summary for the trip and up to three restaurant suggestions.\n"
            f"Destination: {trip.destination}\n"
            f"Days: {trip.days}\n"
            f"Travelers: {trip.travelers}\n"
            f"Budget: {trip.budget}\n"
            f"Interests: {trip.interests}\n"
            f"Travel style: {trip.travel_style}\n"
            "Return the first line as a summary, then each restaurant on a new line in the format: Name | Cuisine | PriceRange (e.g., Bistro du Coin | French | $$)."
        )
        response = gemini_generate(
            client=client,
            model=settings.GEMINI_MODEL,
            contents=prompt,
        )
        content = response.text.strip()
        lines = [line.strip() for line in content.splitlines() if line.strip()]
        summary = lines[0] if lines else ""
        recommendations = []
        for line in lines[1:]:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 3:
                name, cuisine, price = parts[0], parts[1], parts[2]
                rec = {"name": name, "cuisine": cuisine, "price": price}
            else:
                # Fallback: treat whole line as name only
                rec = {"name": line}
            recommendations.append(rec)
        return {"recommendations": recommendations, "summary": summary}
