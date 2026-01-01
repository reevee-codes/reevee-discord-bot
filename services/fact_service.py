import requests
from errors.command_error import CommandError

class FactService:

    def get_random_fact(self):
        url = "https://uselessfacts.jsph.pl/api/v2/facts/random"

        try:
            response = requests.get(url, timeout=5)
        except requests.RequestException:
            raise CommandError("Nie udało się połączyć z API")

        if response.status_code != 200:
            raise CommandError("API zwróciło błąd")

        data = response.json()
        return data["text"]
