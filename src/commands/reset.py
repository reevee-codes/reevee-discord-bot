from src.commands.base import Command
from src.services.ai_service import AiService


class ResetCommand(Command):
    trigger = "!reset"

    def __init__(self, ai_service: AiService):
        self.ai_service = ai_service

    async def execute(self, message, args):
        user_id = message.author.id
        self.ai_service.reset_user(user_id)

        await message.channel.send(
            "Zresetowałem rozmowę i zapamiętane fakty. Zaczynamy od zera!"
        )
