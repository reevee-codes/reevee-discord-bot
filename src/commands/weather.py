from src.commands.base import Command
from src.services.weather_service import WeatherService


class WeatherCommand(Command):
    trigger = "!weather"

    def __init__(self, weather_service: WeatherService):
        self.weather_service = weather_service

    async def execute(self, message, args):
        weather = self.weather_service.getWeather()

        if not weather:
            await message.channel.send("Pogoda się wykrzaczyła")
            return

        text = f"Pogoda w Gdańsku to {weather}°C"
        await message.channel.send(text)
