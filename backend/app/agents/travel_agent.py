import os
import json
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()


class TravelAgent:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")

        # Initialize Gemini client
        self.client = genai.Client(api_key=api_key)

        # Model used for TripMind reasoning
        self.model = "gemini-2.5-flash"

    def generate_itinerary(self, destination: str, days: int, interests: list):
        """
        Generate a structured travel itinerary using Gemini.
        """

        prompt = f"""
You are TripMind, an AI travel planner.

Create a {days}-day travel itinerary for {destination}.

User interests:
{interests}

Return ONLY valid JSON in this format:

{{
  "days": [
    {{
      "day": 1,
      "morning": "",
      "afternoon": "",
      "evening": ""
    }}
  ]
}}

Do not include explanations.
Do not include markdown.
Only return JSON.
Return valid JSON only. Do not include text before or after JSON.
"""

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )

            text = response.text.strip()

            # Try parsing JSON safely
            itinerary_json = json.loads(text)

            return itinerary_json

        except json.JSONDecodeError:
            return {
                "error": "Gemini returned invalid JSON",
                "raw_output": text
            }

        except Exception as e:
            return {
                "error": str(e)
            }