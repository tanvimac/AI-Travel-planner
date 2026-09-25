from .base import Agent
from google import genai
from app.core.config import settings
from app.core.gemini_retry import gemini_generate

class DestinationAgent(Agent):
    """Stub agent that returns a static destination research result."""

    def run(self, context: dict) -> dict:
        trip = context.get("trip")
        if not trip:
            return {"highlights": [], "description": ""}
        # Initialise Gemini client with API key from settings
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        # Build a concise prompt using trip details
        prompt = (
            f"You are a travel guide. Provide a short research summary for a trip with the following details:\n"
            f"Destination: {trip.destination}\n"
            f"Days: {trip.days}\n"
            f"Travelers: {trip.travelers}\n"
            f"Budget: {trip.budget}\n"
            f"Interests: {trip.interests}\n"
            f"Travel style: {trip.travel_style}\n"
            "Give a brief description (2-3 sentences) and three highlights (landmarks, weather, tip)."
        )
        # Call Gemini model
        response = gemini_generate(
            client=client,
            model=settings.GEMINI_MODEL,
            contents=prompt,
        )
        content = response.text.strip()
        # Simple parsing: first non-empty line = description, following lines = highlights
        lines = [line for line in content.splitlines() if line.strip()]
        description = lines[0] if lines else ""
        highlights = [line.lstrip("- *").strip() for line in lines[1:] if line.strip()]
        return {"highlights": highlights, "description": description}
