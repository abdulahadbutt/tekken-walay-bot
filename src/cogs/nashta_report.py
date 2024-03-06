from discord.ext import commands, tasks
# import discord 
# import os 
from datetime import datetime, timedelta


nashta_members = open('nashta_report_members.txt', 'r').readlines()
nashta_members = [x.strip() for x in nashta_members]

nashta_time = (datetime.utcnow() + timedelta(minutes=2)).time()
print(f'NASHTA TIME')



class NashtaReport(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        print('LOADING NASHTA REPORT...')

        super().__init__()
        self.bot = bot 
        # self.index = 0
        self.print_nashta_report.start()

        print('LOADED NASHTA REPORT...')

    @tasks.loop(time=nashta_time)
    async def print_nashta_report(self):
        print('IT IS NASHTA TIME')
        # self.index += 1


async def setup(bot: commands.Bot):
    await bot.add_cog(NashtaReport(bot))