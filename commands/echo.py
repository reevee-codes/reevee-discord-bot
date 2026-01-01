from commands.base import Command
from services.echo_service import EchoService

class EchoCommand(Command):
    trigger = "!echo"

    def __init__(self):
        self.echo_service = EchoService()

    async def execute(self, message, args):
        text = self.echo_service.build_echo_text(args)
        if text is None:
            await message.channel.send("Musisz podać tekst do echo")
            return
        await message.channel.send(text)