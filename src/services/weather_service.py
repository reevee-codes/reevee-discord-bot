import requests
from src.errors.command_error import CommandError

class WeatherService:

    def getWeather(self):
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": 54.35,
            "longitude": 18.65,
            "current_weather": True
        }
        try:
            response = requests.get(url, params=params)
        except requests.RequestException:
            raise CommandError("No connection to API")

        if response.status_code != 200:
            raise CommandError("API returned error")

        temp = response.json()["current_weather"]["temperature"]
        return temp
