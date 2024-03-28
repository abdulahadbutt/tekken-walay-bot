from discord.ext import commands, tasks
import discord 
import os 
import logging
import json 


logger = logging.getLogger('discord')


class OnMessageCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        logger.info("LOADING ON MESSAGE COMMANDS...")
        self.bot = bot
        self.replies_dict = json.load(open('replies.json'))
        logger.info('LOADED ON MESSAGE COMMANDS...')

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return 
        
        message_content = message.content
        if message_content not in self.replies_dict:
            return 
        
        payload = self.replies_dict[message_content]
        message_response = payload['response']
        mention_user = payload['mention_user']

        if mention_user:
            # message_response += f" <@{message.author.id}>"
            message_response = f"<@{message.author.id}> {message_response}"
        await message.channel.send(message_response)


async def setup(bot: commands.Bot):
    await bot.add_cog(OnMessageCommands(bot))