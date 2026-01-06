import discord

class Command:

    async def execute(self, message: discord.Message, args):
        raise NotImplementedError("!")
