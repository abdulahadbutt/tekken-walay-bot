from discord.ext import commands, tasks
import discord 
import os 
# from datetime import datetime, timedelta
import datetime 
import logging

logger = logging.getLogger('discord')


TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
AFTAARI_CHANNEL_ID = os.getenv('AFTAARI_CHANNEL_ID')

iftaari_members = open('nashta_report_members.txt', 'r').readlines()
iftaari_members = [x.strip() for x in iftaari_members]

# aftaari_time = (datetime.datetime.utcnow() + datetime.timedelta(minutes=1)).time()
aftaari_time = datetime.time(hour=13, minute=30, tzinfo=datetime.timezone.utc)
logger.info(f'AFTAARI TIME: {aftaari_time}')

class AftaariReport(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        logger.info('LOADING AFTAARI REPORT...')

        super().__init__()
        self.bot = bot 
        self.print_aftaari_report.start()
        
        logger.info('LOADED AFTAARI REPORT...')


    def cog_unload(self):
        self.print_aftaari_report.cancel()


    # @tasks.loop(seconds=5.0, count=1)
    @tasks.loop(time=aftaari_time)
    async def print_aftaari_report(self):
        all_members = self.guild.members 
        n_members = [x for x in all_members if x.name in iftaari_members]
        message_content = [x.id for x in n_members]
        message_content = [f'<@{x}>' for x in message_content]

        self.channel = None
        for channel in self.guild.text_channels:
            if channel.name == 'general':
                logger.info(repr(channel))
                self.channel = channel


        msg = "Aftaari Report " + " ".join(message_content)
        await self.channel.send(msg)


    @print_aftaari_report.before_loop
    async def before_print_aftaari_report(self):
        logger.info('PRELOADING AFTAARI REPORT...')
        await self.bot.wait_until_ready()

        # logger.info('all guilds')
        # logger.info(self.bot.guilds)
        self.guild = discord.utils.get(self.bot.guilds, name=GUILD)
        logger.info(f'guild selected: {self.guild}')
        # logger.info('specific guild: ')
        # logger.info(self.guild)
        logger.info('AFTAARI REPORT PRELOADED...')


async def setup(bot: commands.Bot):
    await bot.add_cog(AftaariReport(bot))