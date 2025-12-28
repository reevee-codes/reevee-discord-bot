from commands.base import Command
from services.quote_service import QuoteService

class QuoteCommand(Command):
    trigger = "!quote"

    def __init__(self):
        self.quote_service = QuoteService()

    async def execute(self, message, args):
        quote = self.quote_service.random_quote()

        await message.channel.send(quote)