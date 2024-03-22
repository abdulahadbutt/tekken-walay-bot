from discord.ext import commands, tasks
import discord 
import os 
# from datetime import datetime, timedelta
import datetime 
import logging

logger = logging.getLogger('discord')


TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

sehri_members = open('nashta_report_members.txt', 'r').readlines()
sehri_members = [x.strip() for x in sehri_members]

# sehri_time = (datetime.datetime.utcnow() + datetime.timedelta(minutes=2)).time()
sehri_time = datetime.time(hour=0, tzinfo=datetime.timezone.utc)
logger.info(f'SEHRI TIME: {sehri_time}')

class SehriReport(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        logger.info('LOADING SEHRI REPORT...')

        super().__init__()
        self.bot = bot 
        self.print_sehri_report.start()
        
        logger.info('LOADED SEHRI REPORT...')


    def cog_unload(self):
        self.print_sehri_report.cancel()


    # @tasks.loop(seconds=5.0, count=1)
    @tasks.loop(time=sehri_time)
    async def print_sehri_report(self):
        all_members = self.guild.members 
        n_members = [x for x in all_members if x.name in sehri_members]
        message_content = [x.id for x in n_members]
        message_content = [f'<@{x}>' for x in message_content]

        self.channel = None
        for channel in self.guild.text_channels:
            if channel.name == 'general':
                logger.info(repr(channel))
                self.channel = channel


        msg = "Sehri Report " + " ".join(message_content)
        await self.channel.send(msg)


    @print_sehri_report.before_loop
    async def before_print_sehri_report(self):
        logger.info('PRELOADING SEHRI...')
        await self.bot.wait_until_ready()

        # logger.info('all guilds')
        # logger.info(self.bot.guilds)
        self.guild = discord.utils.get(self.bot.guilds, name=GUILD)

        # logger.info('specific guild: ')
        # logger.info(self.guild)
        logger.info('SEHRI PRELOADED...')


async def setup(bot: commands.Bot):
    await bot.add_cog(SehriReport(bot))