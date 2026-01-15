import discord
import os
from dotenv import load_dotenv

from src.commands.chat import ChatCommand
from src.commands.fact import FactCommand
from src.commands.facts import FactsCommand
from src.commands.ping import PingCommand
from src.commands.echo import EchoCommand
from src.commands.quote import QuoteCommand
from src.services.ai_service import AiService

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
ai_service = AiService()
commands = [PingCommand(), EchoCommand(), QuoteCommand(), FactCommand(), ChatCommand(ai_service),
            FactsCommand(ai_service)]

@client.event
async def on_ready():
    print("Discord bot started running.")

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