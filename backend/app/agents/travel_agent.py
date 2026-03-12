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

        # Model used
        self.model = "gemini-2.5-flash"

        # Tools
        self.place_finder = PlaceFinder()
        self.weather_tool = WeatherTool()

    def generate_itinerary(self, destination: str, days: int, interests: list):

        try:

            # --------------------------------
            # Interest → Google Places mapping
            # --------------------------------
            category_map = {
                "beaches": "beaches",
                "cafes": "cafes",
                "restaurants": "restaurants",
                "food": "restaurants",
                "nightlife": "bars",
                "bars": "bars",
                "monuments": "tourist attractions",
                "history": "tourist attractions",
                "culture": "tourist attractions",
                "hotels": "hotels",
                "hostels": "hostels",
                "nature": "parks"
            }

            categories = []

            for interest in interests:
                interest = interest.lower()
                if interest in category_map:
                    categories.append(category_map[interest])

            # Always include these useful categories
            categories.extend([
                "restaurants",
                "tourist attractions"
            ])

            # Remove duplicates
            categories = list(set(categories))

            # --------------------------------
            # Fetch places from Google Places
            # --------------------------------
            places_data = {}

            for category in categories:
                places_data[category] = self.place_finder.find_places(
                    destination,
                    category
                )

            # Extract place names for prompt
            place_summary = {}

            for category, places in places_data.items():
                place_summary[category] = places

            # --------------------------------
            # Fetch weather
            # --------------------------------
            weather_data = self.weather_tool.get_destination_weather(destination)

            weather_info = {
                "temperature": weather_data.get("temperature_celsius"),
                "windspeed": weather_data.get("windspeed_kmh"),
                "condition": weather_data.get("condition")
            }

            # --------------------------------
            # Build Gemini prompt
            # --------------------------------
            prompt = f"""
You are TripMind, an intelligent AI travel planner.

Destination: {destination}
Trip duration: {days} days
User interests: {interests}

Current weather:
Temperature: {weather_info["temperature"]}°C
Condition: {weather_info["condition"]}

Available places by category:
{place_summary}

Instructions:

- ONLY use places listed in "Available places".
- DO NOT invent or guess locations.
- Every activity must reference a place from the provided lists.
- Ensure restaurants and food spots are included for lunch and dinner.
- Balance beaches, attractions, food, and nightlife.

Example structure:

Morning → beach or attraction  
Afternoon → restaurant or cafe  
Evening → bar / nightlife / attraction

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
- Do NOT include explanations
- Do NOT include markdown
- Do NOT include text before or after JSON
"""

            # --------------------------------
            # Call Gemini
            # --------------------------------
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )

            text = response.text.strip()

            itinerary_json = json.loads(text)

            # --------------------------------
            # Final API response
            # --------------------------------
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