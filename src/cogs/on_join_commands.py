from discord.ext import commands, tasks
import discord 
import os 
import logging

logger = logging.getLogger('discord')


TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


class OnJoinCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        logger.info('LOADING ON JOIN COMMANDS...')

        super().__init__()
        self.bot = bot 
        # self.change_username.start()
        
        logger.info('LOADED ON JOIN COMMANDS REPORT...')


    def cog_unload(self):
        self.change_username.cancel()


    @commands.Cog.listener()
    # async def on_member_join(self, member: discord.Member):
    async def on_member_join(self, member: discord.Member):
        logger.info(f'NEW MEMBER JOINED: {member}')
        if member.id == 315568786470076418:
            logger.info('HAMZA JOINED')
            await member.edit(nick="SORE LOSER 99")
            logger.info("nickname changed for Hamza")

        # if member.id == 238338475768676353:
        #     logger.info('CHIMI JOINED')
        #     await member.edit(nick="SORE LOSER 99")
        #     logger.info("nickname changed for Chimi")

        # await member.edit(nick="")/

    # @tasks.loop(seconds=5.0, count=1)
    # @tasks.loop(time=sehri_time)
    # async def change_username(self):
    #     all_members = self.guild.members 
    #     n_members = [x for x in all_members if x.name in sehri_members]
    #     message_content = [x.id for x in n_members]
    #     message_content = [f'<@{x}>' for x in message_content]

    #     self.channel = None
    #     for channel in self.guild.text_channels:
    #         if channel.name == 'general':
    #             logger.info(repr(channel))
    #             self.channel = channel


    #     msg = "Sehri Report " + " ".join(message_content)
    #     await self.channel.send(msg)


    # @change_username.before_loop
    # async def before_print_sehri_report(self):
    #     logger.info('PRELOADING SEHRI...')
    #     await self.bot.wait_until_ready()

    #     # logger.info('all guilds')
    #     # logger.info(self.bot.guilds)
    #     self.guild = discord.utils.get(self.bot.guilds, name=GUILD)

    #     # logger.info('specific guild: ')
    #     # logger.info(self.guild)
    #     logger.info('SEHRI PRELOADED...')


async def setup(bot: commands.Bot):
    await bot.add_cog(OnJoinCommands(bot))