import discord
from discord.ext import commands
import asyncio
from signal import SIGINT, SIGTERM
import os
from dotenv import load_dotenv, find_dotenv
import logging 
import logging.handlers

# ? Loading in the .env file and creating logs directory
load_dotenv(override=True)
os.makedirs('logs', exist_ok=True)

# ? Reading in environment variables
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
NASHTA_CHANNEL_ID = os.getenv('NASHTA_CHANNEL_ID')
COGS_DIR = './src/cogs'


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
logging.getLogger('discord.http').setLevel(logging.INFO)
handler = logging.handlers.RotatingFileHandler(
    filename=f'logs/discord.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=5,  # Rotate through 5 files
)
dt_fmt = '%d-%m-%Y %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
handler.setFormatter(formatter)
logger.addHandler(handler)



async def load_extensions():
    logger.info('loading extensions')
    for filename in os.listdir("./src/cogs"):
        if filename.endswith(".py"):
            # cut off the .py from the file name
            logger.info(f'loading extension: src.cogs.{filename[:-3]}')
            await bot.load_extension(f"cogs.{filename[:-3]}")


# ? On ready decorator
@bot.event
async def on_ready():
    logger.info(f'Logged in as {bot.user}')


# ? Checking message
@bot.event
async def on_message(message):
    # ? Stopping reading bot's own messages
    if message.author == bot.user:
        return
    
    # ? Simple command to check if bot is online
    if message.content.startswith('$hello'):
        logger.info("User used $hello")
        await message.channel.send('Hello!')


async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info('\nExiting...')
    # client.run(TOKEN, log_handler=None)
