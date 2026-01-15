from src.commands.base import Command
from src.services.ai_service import AiService


class FactsCommand(Command):
    trigger = "!facts"

    def __init__(self, ai_service: AiService):
        self.ai_service = ai_service

    async def execute(self, message, args):
        user_id = message.author.id
        facts = self.ai_service.get_facts(user_id)

        if not facts:
            await message.channel.send("Na razie nic o Tobie nie wiem.")
            return

        text = "**Wiem o Tobie:**\n" + "\n".join(f"- {fact}" for fact in facts)
        await message.channel.send(text)
