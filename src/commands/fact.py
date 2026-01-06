from src.commands.base import Command
from src.errors.command_error import CommandError
from src.services.fact_service import FactService

class FactCommand(Command):
    trigger = "!fact"

    def __init__(self):
        self.fact_service = FactService()

    async def execute(self, message, args):
        try:
            text = self.fact_service.get_random_fact()
            await message.channel.send(text)
        except CommandError as e:
            await message.channel.send(str(e))
