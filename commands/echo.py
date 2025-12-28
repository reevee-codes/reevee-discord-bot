from commands.base import Command
from services.echo_service import EchoService

class EchoCommand(Command):
    trigger = "!echo"

    def __init__(self):
        self.echo_service = EchoService()

    async def execute(self, message, args):
        await message.channel.send(self.echo_service.build_echo_text(args))