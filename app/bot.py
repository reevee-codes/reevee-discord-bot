import discord
import os
from dotenv import load_dotenv
from commands.ping import PingCommand
from commands.echo import EchoCommand
from commands.quote import QuoteCommand

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
commands = [PingCommand(), EchoCommand(), QuoteCommand()]

@client.event
async def on_ready():
    print("Discord bot started running!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    content = message.content.strip()
    parts = content.split(" ")
    if not parts:
        return
    input_command = parts[0]
    rest_of_args = parts[1:]

    for command in commands:
        if input_command == command.trigger:
            await command.execute(message, rest_of_args)
            break
client.run(TOKEN)