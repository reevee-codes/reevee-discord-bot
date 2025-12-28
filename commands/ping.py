from commands.base import Command

class PingCommand(Command):
    trigger = "!ping"

    async def execute(self, message, args):
        await message.channel.send('Pong!')