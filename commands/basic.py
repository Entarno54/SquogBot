import nextcord
from nextcord.ext import commands

class Main():
    def __init__(self, bot):
        self.client = bot

    @commands.command()
    async def help(self, ctx: nextcord.Message):
        embed = nextcord.Embed(title="Help")
        for command in self.client.commands:
            embed.add_field(name=command.name, value=f"Arguments: {command.usage} \nDescription: {command.description}")
        await ctx.reply(embed=embed)

    @commands.command(description="Check how fast the bot will reply to you.")
    async def ping(ctx: nextcord.Message):
        await ctx.reply("Pong!")


def setup(bot):
    Main(bot)