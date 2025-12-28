from services.quotes_data import QUOTES
import random

class QuoteService:

    def random_quote(self):
        return random.choice(QUOTES)