import discord
import os
from dotenv import load_dotenv

from src.commands.add_todo import AddTodoCommand
from src.commands.chat import ChatCommand
from src.commands.fact import FactCommand
from src.commands.facts import FactsCommand
from src.commands.get_todo import GetTodoCommand
from src.commands.ping import PingCommand
from src.commands.echo import EchoCommand
from src.commands.quote import QuoteCommand
from src.commands.reset import ResetCommand
from src.commands.weather import WeatherCommand
from src.memory.sqlite_memory_store import SqliteMemoryStore
from src.services.ai_service import AiService
from src.services.weather_service import WeatherService

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

memory_store = SqliteMemoryStore()
ai_service = AiService(memory_store)
weather_service = WeatherService()
commands = [PingCommand(), EchoCommand(), QuoteCommand(), FactCommand(), ChatCommand(ai_service),
            FactsCommand(memory_store), WeatherCommand(weather_service),
            ResetCommand(ai_service), GetTodoCommand(memory_store),
            AddTodoCommand(memory_store)]

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