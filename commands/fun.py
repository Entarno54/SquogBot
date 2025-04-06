import nextcord
from nextcord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    # Add something here later cuz im lazy raaahhh

def setup(bot):
    bot.add_cog(Fun(bot))