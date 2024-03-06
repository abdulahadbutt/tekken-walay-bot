import discord
from discord.ext import commands
import asyncio
from signal import SIGINT, SIGTERM
import os
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
NASHTA_CHANNEL_ID = 889139268486828054
COGS_DIR = './src/cogs'

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)


async def load_extensions():
    print('loading extensions')
    for filename in os.listdir("./src/cogs"):
        if filename.endswith(".py"):
            # cut off the .py from the file name
            print(f'loading extension: src.cogs.{filename[:-3]}')
            await bot.load_extension(f"cogs.{filename[:-3]}")


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')



@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')


async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('\nExiting...')
    # client.run(TOKEN, log_handler=None)
