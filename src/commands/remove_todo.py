from src.commands.base import Command


class RemoveTodoCommand(Command):
    trigger = "!remove_todo"

    def __init__(self, memory_store):
        self.memory_store = memory_store

    async def execute(self, message, args):
        """
    to be implemented
        """
