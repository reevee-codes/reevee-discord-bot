from src.commands.base import Command
from src.errors.command_error import CommandError
from src.services.echo_service import EchoService

class EchoCommand(Command):
    trigger = "!echo"

    def __init__(self):
        self.echo_service = EchoService()

    async def execute(self, message, args):
        try:
            text = self.echo_service.build_echo_text(args)
            await message.channel.send(text)
        except CommandError as e:
            await message.channel.send(str(e))
