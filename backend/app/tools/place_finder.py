from app.services.places_service import PlacesService


class PlaceFinder:

    def __init__(self):
        self.service = PlacesService()

    def find_places(self, destination: str, category: str):
        """
        Find places using Google Places API
        """

        places = self.service.search_places(category, destination)

        return places

    def find_multiple_categories(self, destination: str, categories: list):
        """
        Fetch multiple place categories
        """

        results = {}

        for category in categories:
            results[category] = self.service.search_places(category, destination)

        return results