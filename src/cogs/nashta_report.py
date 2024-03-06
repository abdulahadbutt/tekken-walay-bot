from discord.ext import commands, tasks
import discord 
import os 
from datetime import datetime, timedelta

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
NASHTA_CHANNEL_ID = os.getenv('NASHTA_CHANNEL_ID')

nashta_members = open('nashta_report_members.txt', 'r').readlines()
nashta_members = [x.strip() for x in nashta_members]

nashta_time = (datetime.utcnow() + timedelta(minutes=2)).time()



class NashtaReport(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        print('LOADING NASHTA REPORT...')

        super().__init__()
        self.bot = bot 
        self.print_nashta_report.start()
        
        print('LOADED NASHTA REPORT...')


    def cog_unload(self):
        self.print_nashta_report.cancel()


    @tasks.loop(seconds=5.0, count=1)
    # @tasks.loop(time=nashta_time)
    async def print_nashta_report(self):
        all_members = self.guild.members 
        n_members = [x for x in all_members if x.name in nashta_members]
        message_content = [x.id for x in n_members]
        message_content = [f'<@{x}>' for x in message_content]

        self.channel = None
        for channel in self.guild.text_channels:
            if channel.name == 'general':
                print(repr(channel))
                self.channel = channel

        # channel = self.guild.get_channel(NASHTA_CHANNEL_ID)

        msg = "Nashta Report " + " ".join(message_content)
        # print(msg)
        await self.channel.send(msg)


    @print_nashta_report.before_loop
    async def before_print_nashta_report(self):
        print('waiting...')
        await self.bot.wait_until_ready()

        print('all guilds')
        print(self.bot.guilds)
        self.guild = discord.utils.get(self.bot.guilds, name=GUILD)

        print('specific guild: ')
        print(self.guild)
        print('guild loaded...')


async def setup(bot: commands.Bot):
    await bot.add_cog(NashtaReport(bot))