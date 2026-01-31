from src.commands.base import Command

class GetTodoCommand(Command):
    trigger = "!get_todo"

    def __init__(self, memory_store):
        self.memory_store = memory_store

    async def execute(self, message, args):
        user_id = message.author.id
        todo = self.memory_store.get_todo(user_id)

        if not todo:
            await message.channel.send("Na razie nie masz nic w todo!")
            return

        lines = "\n".join(f"• {x}" for x in todo)
        await message.channel.send(f"Masz do roboty:\n{lines}")