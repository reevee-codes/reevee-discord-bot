from src.commands.base import Command


class FactsCommand(Command):
    trigger = "!facts"

    def __init__(self, memory_store):
        self.memory_store = memory_store

    async def execute(self, message, args):
        user_id = message.author.id
        facts = self.memory_store.get_facts(user_id)

        if not facts:
            await message.channel.send("Na razie nic o Tobie nie wiem 🙂")
            return

        lines = "\n".join(f"• {fact}" for fact in facts.values())
        await message.channel.send(f"Wiem o Tobie:\n{lines}")