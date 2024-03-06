from discord.ext import commands, tasks
import discord 
import os 

nashta_members = open('nashta_report_members.txt', 'r').readlines()
nashta_members = [x.strip() for x in nashta_members]


class NashtaReport(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        print('LOADED NASHTA REPORT...')

        super().__init__()
        self.bot = bot 
        self.index = 0
        self.print_nashta_report.start()


    @tasks.loop(minutes=1.0)
    async def print_nashta_report(self):
        print(self.index)
        self.index += 1


async def setup(bot: commands.Bot):
    await bot.add_cog(NashtaReport(bot))