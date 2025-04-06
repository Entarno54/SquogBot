import nextcord
from nextcord.ext import commands

class Logger(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.Cog.listener
    async def on_message_delete(self, msg: nextcord.Message):
        embed = nextcord.Embed(
            title="Message delete",
            description=msg.content
        )
        embed.set_author(name=msg.author.name)
        for image in msg.attachments:
            embed.set_image(image.url)  # Unfortunately i cant add multiple images.
        await SquogMod.send(embed=embed)

    @commands.Cog.listener
    async def on_command(self, ctx: commands.Context):
        embed = nextcord.Embed(
            title="Command used",
            description=ctx.message.content
        )
        field = embed.add_field(name="Channel", value=ctx.channel.name)
        await SquogMod.send(embed=embed)

    @commands.Cog.listener
    async def on_ready(self):
        global SquogMod
        print("Bot logged")
        SquogMod = self.client.get_channel(1356577069068324986)
        print(SquogMod)

def setup(bot):
    bot.add_cog(Logger(bot))