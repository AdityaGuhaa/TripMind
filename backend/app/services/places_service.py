import os
import requests
from dotenv import load_dotenv

load_dotenv()

PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")


class PlacesService:

    BASE_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"

    def search_places(self, query, location):

        params = {
            "query": f"{query} in {location}",
            "key": PLACES_API_KEY
        }

        response = requests.get(self.BASE_URL, params=params)

        if response.status_code != 200:
            return []

        data = response.json()

        places = []

        for place in data.get("results", [])[:5]:
            places.append({
                "name": place.get("name"),
                "address": place.get("formatted_address"),
                "rating": place.get("rating")
            })

        return places