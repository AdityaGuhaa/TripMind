import os
import json
from dotenv import load_dotenv
from google import genai

from app.tools.place_finder import PlaceFinder
from app.tools.weather_tool import WeatherTool

# Load environment variables
load_dotenv()


class TravelAgent:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")

        # Gemini client
        self.client = genai.Client(api_key=api_key)

        # Model
        self.model = "gemini-2.5-flash"

        # Tools
        self.place_finder = PlaceFinder()
        self.weather_tool = WeatherTool()

    def generate_itinerary(self, destination: str, days: int, interests: list):

        try:

            # -----------------------------
            # Fetch places
            # -----------------------------
            cafes_data = self.place_finder.find_places(destination, "cafes")
            beaches_data = self.place_finder.find_places(destination, "beaches")

            cafes = [place["name"] for place in cafes_data]
            beaches = [place["name"] for place in beaches_data]

            # -----------------------------
            # Fetch weather
            # -----------------------------
            weather_data = self.weather_tool.get_destination_weather(destination)

            weather_info = {
                "temperature": weather_data.get("temperature_celsius"),
                "windspeed": weather_data.get("windspeed_kmh"),
                "condition": weather_data.get("condition")
            }

            # -----------------------------
            # Build prompt
            # -----------------------------
            prompt = f"""
You are TripMind, an intelligent AI travel planner.

Destination: {destination}
Trip duration: {days} days
User interests: {interests}

Current weather:
Temperature: {weather_info["temperature"]}°C
Condition: {weather_info["condition"]}

Available cafes:
{cafes}

Available beaches:
{beaches}

Instructions:

- Use ONLY the places listed above.
- If weather suggests rain or storms, avoid beaches.
- If weather is clear or sunny, prioritize beaches.
- Balance activities across the trip.

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

Rules:
- No explanations
- No markdown
- No text before or after JSON
"""

            # -----------------------------
            # Call Gemini
            # -----------------------------
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )

            text = response.text.strip()

            itinerary_json = json.loads(text)

            # -----------------------------
            # Final response
            # -----------------------------
            return {
                "destination": destination,
                "weather": weather_info,
                "itinerary": itinerary_json
            }

        except json.JSONDecodeError:
            return {
                "error": "Gemini returned invalid JSON",
                "raw_output": text
            }

        except Exception as e:
            return {
                "error": str(e)
            }