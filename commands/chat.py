from commands.base import Command
from errors.command_error import CommandError
from services.ai_service import AiService

class ChatCommand(Command):
    trigger = "!chat"

    def __init__(self):
        self.ai_service = AiService()

    async def execute(self, message, args):
        user_text = " ".join(args)
        try:
            reply = await self.ai_service.ask(user_text)
            await message.channel.send(reply)
        except CommandError as e:
            await message.channel.send(str(e))
