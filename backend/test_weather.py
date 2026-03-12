from app.services.weather_service import WeatherService

service = WeatherService()

# Goa coordinates
weather = service.get_weather(15.2993, 74.1240)

print("\nWeather Data:\n")
print(weather)
