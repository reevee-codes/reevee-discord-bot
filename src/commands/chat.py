from src.commands.base import Command
from src.errors.command_error import CommandError
from src.services.ai_service import AiService

class ChatCommand(Command):
    trigger = "!chat"

    def __init__(self, ai_service: AiService):
        self.ai_service = ai_service

    async def execute(self, message, args):
        user_text = " ".join(args)
        try:
            user_id = message.author.id
            reply = await self.ai_service.ask(user_id, user_text)
            if not reply or not reply.strip():
                reply = "Jestem tu 🙂 Możesz powiedzieć trochę więcej?"
            await message.channel.send(reply)
        except CommandError as e:
            await message.channel.send(str(e))
