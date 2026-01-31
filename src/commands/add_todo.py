from src.commands.base import Command

class AddTodoCommand(Command):
    trigger = "!add_todo"

    def __init__(self, memory_store):
        self.memory_store = memory_store

    async def execute(self, message, args):
        user_id = message.author.id
        item = args.strip()
        todo = self.memory_store.add_todo(user_id, item)

        if not todo:
            await message.channel.send("Musisz coś wpisać, żeby dało się to dodać do todo!")
            return

        lines = "\n".join(f"• {x}" for x in todo.values())
        await message.channel.send(f"Dodane! Poza tym masz do roboty:\n{lines}")