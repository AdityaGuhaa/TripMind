from app.services.weather_service import WeatherService


class WeatherTool:

    def __init__(self):
        self.weather_service = WeatherService()

        # Temporary destination → coordinates map
        self.coordinates = {
            "Goa": (15.2993, 74.1240),
            "Mumbai": (19.0760, 72.8777),
            "Delhi": (28.6139, 77.2090)
        }

    def get_destination_weather(self, destination: str):

        lat, lon = self.coordinates.get(destination, (15.2993, 74.1240))

        weather = self.weather_service.get_weather(lat, lon)

        return weather