from .base import Agent
from google import genai
from app.core.config import settings
from app.core.gemini_retry import gemini_generate

class HotelAgent(Agent):
    """Hotel recommendation agent using Gemini LLM."""

    def run(self, context: dict) -> dict:
        trip = context.get('trip')
        if not trip:
            return {"recommendations": [], "summary": ""}
        # Initialise Gemini client
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        # Build prompt with trip details
        prompt = (
            f"You are a travel planner. Provide a brief hotel recommendation summary for a trip and up to three hotel suggestions.\n"
            f"Destination: {trip.destination}\n"
            f"Days: {trip.days}\n"
            f"Travelers: {trip.travelers}\n"
            f"Budget: {trip.budget}\n"
            f"Interests: {trip.interests}\n"
            f"Travel style: {trip.travel_style}\n"
            "Return the first line as a summary, then each hotel on a new line in the format: Name | PriceRange | Rating (e.g., Hotel Alpha | $$ | 4.5)."
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
                name, price_range, rating_str = parts[0], parts[1], parts[2]
                try:
                    rating = float(rating_str)
                except ValueError:
                    rating = None
                rec = {"name": name, "price_range": price_range}
                if rating is not None:
                    rec["rating"] = rating
                recommendations.append(rec)
            else:
                recommendations.append({"name": line})
        return {"recommendations": recommendations, "summary": summary}
