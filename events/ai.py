import nextcord
from nextcord.ext import commands
import requests

class AI(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot

    @commands.Cog.listener()
    async def on_message_create(self, message: nextcord.Message):
        print(message.content)
        self.client.process_application_commands(message)

def setup(bot):
    bot.add_cog(AI(bot))