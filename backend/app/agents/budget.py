import json
import logging
import re
from .base import Agent
from google import genai
from google.genai import types
from app.core.config import settings
from app.core.gemini_retry import gemini_generate

logger = logging.getLogger("budget_agent")


def _clean_json_string(text: str) -> str:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned.strip()


class BudgetAgent(Agent):
    """Budget estimation agent using Gemini LLM."""

    def run(self, context: dict) -> dict:
        trip = context.get('trip')
        if not trip:
            return {"total_estimated": 0, "details": {}}
        # Initialise Gemini client
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        # Build a prompt that asks Gemini to provide a budget breakdown in JSON format.
        prompt = (
            f"You are a travel planner. Provide a practical budget breakdown for the upcoming trip.\n"
            f"Destination: {trip.destination}\n"
            f"Days: {trip.days}\n"
            f"Travelers: {trip.travelers}\n"
            f"Total budget: {trip.budget}\n"
            f"Interests: {trip.interests}\n"
            f"Travel style: {trip.travel_style}\n"
            "If the context already contains results from hotel, food, or activity agents, you may incorporate them, but keep the output simple.\n"
            "Return ONLY a JSON object with the following structure: \n"
            "{\n"
            "  \"total_estimated\": <float>,\n"
            "  \"details\": {\n"
            "    \"flights\": <float>,\n"
            "    \"accommodation\": <float>,\n"
            "    \"food\": <float>,\n"
            "    \"activities\": <float>,\n"
            "    \"miscellaneous\": <float>\n"
            "  }\n"
            "}\n"
            "Do not include any explanatory text outside the JSON."
        )
        response = gemini_generate(
            client=client,
            model=settings.GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(response_mime_type="application/json"),
        )
        content = response.text.strip()
        cleaned_content = _clean_json_string(content)
        data = None
        try:
            data = json.loads(cleaned_content)
        except json.JSONDecodeError:
            # Fallback: try to extract JSON-like substring
            start = cleaned_content.find('{')
            end = cleaned_content.rfind('}') + 1
            if start != -1 and end > start:
                try:
                    data = json.loads(cleaned_content[start:end])
                except Exception as exc:
                    logger.warning("BudgetAgent failed to extract JSON substring: %s. Raw: %r", exc, content)
            if data is None:
                logger.warning("BudgetAgent failed to parse Gemini JSON output. Raw content: %r", content)
                data = {"total_estimated": 0, "details": {}}

        # Ensure required keys exist
        total = data.get("total_estimated", 0)
        details = data.get("details", {})
        return {"total_estimated": total, "details": details}
