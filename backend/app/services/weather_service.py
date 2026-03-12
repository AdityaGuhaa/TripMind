import requests


class WeatherService:
    """
    Weather service using Open-Meteo API
    """

    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    WEATHER_CODES = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow fall",
        73: "Moderate snow fall",
        75: "Heavy snow fall",
        80: "Rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        95: "Thunderstorm"
    }

    def get_weather(self, latitude: float, longitude: float):
        """
        Fetch current weather for given coordinates
        """

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current_weather": True
        }

        try:
            response = requests.get(
                self.BASE_URL,
                params=params,
                timeout=5
            )

            response.raise_for_status()

            data = response.json()

            weather = data.get("current_weather")

            if not weather:
                return {
                    "error": "Weather data unavailable"
                }

            code = weather.get("weathercode")

            return {
                "temperature_celsius": weather.get("temperature"),
                "windspeed_kmh": weather.get("windspeed"),
                "weather_code": code,
                "condition": self.WEATHER_CODES.get(code, "Unknown")
            }

        except requests.exceptions.Timeout:
            return {
                "error": "Weather API timeout"
            }

        except requests.exceptions.RequestException as e:
            return {
                "error": str(e)
            }