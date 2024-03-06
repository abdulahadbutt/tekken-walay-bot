import discord
import os
from dotenv import load_dotenv
import logging 
import logging.handlers
from datetime import datetime, time, timedelta
import asyncio
import threading


load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
WHEN = time(13, 39, 0)
NASHTA_CHANNEL_ID = 889139268486828054

os.makedirs('logs', exist_ok=True)


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

nashta_members = open('nashta_report_members.txt', 'r').readlines()
nashta_members = [x.strip() for x in nashta_members]


curr_datetime = datetime.now().strftime('%H:%M %d_%m_%Y')
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
logging.getLogger('discord.http').setLevel(logging.INFO)



handler = logging.handlers.RotatingFileHandler(
    filename=f'logs/{curr_datetime}.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=5,  # Rotate through 5 files
)

logger.addHandler(handler)


# ? FIRED EVERYDAY
async def nastha_report(client: discord.Client):
    await client.wait_until_ready()

    guild=discord.utils.get(client.guilds, name=GUILD)
    all_members = guild.members 

    n_members = [x for x in all_members if x.name in nashta_members]
    message_content = [x.id for x in n_members]
    message_content = [f'<@{x}>' for x in message_content]

    channel = guild.get_channel(NASHTA_CHANNEL_ID)

    await channel.send(" ".join(message_content))


async def background_task():
    now = datetime.utcnow()
    if now.time() > WHEN:
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        seconds = (tomorrow - now).total_seconds()
        await asyncio.sleep(seconds) 

    while True:
        now = datetime.utcnow()
        target_time = datetime.combine(now.date(), WHEN)
        print(f'target time: {target_time}')
        seconds_until_target = (target_time - now).total_seconds()
        await asyncio.sleep(seconds_until_target)
        await nastha_report()
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        seconds = (tomorrow - now).total_seconds()
        await asyncio.sleep(seconds)


@client.event
async def on_ready():
    logger.info(f'We have logged in as {client.user}')



@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')



if __name__ == '__main__':
    client.run(TOKEN, log_handler=None)
