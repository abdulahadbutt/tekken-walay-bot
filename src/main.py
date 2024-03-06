import discord
import os
from dotenv import load_dotenv
import logging 
import logging.handlers
from datetime import datetime

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
os.makedirs('logs', exist_ok=True)


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)



curr_datetime = datetime.now().strftime('%H:%M %d_%m_%Y')
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logging.getLogger('discord.http').setLevel(logging.INFO)



handler = logging.handlers.RotatingFileHandler(
    filename=f'logs/{curr_datetime}.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=5,  # Rotate through 5 files
)

logger.addHandler(handler)


@client.event
async def on_ready():
    logger.info(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(TOKEN, log_handler=None)
