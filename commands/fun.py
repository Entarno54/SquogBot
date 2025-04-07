import os
import random

import nextcord
from nextcord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command(description="Boop the user of your desire", usage={"@user"})
    async def boop(self, ctx: nextcord.Message, user: nextcord.User):
        await ctx.reply(f"{user.mention} shall get booped!", files=[nextcord.File("./images/boop.webp")])

    @commands.command(description="Turn someone into a squog", usage={"@user"})
    async def squogify(self, ctx: nextcord.Message, user: nextcord.User):
        await ctx.reply(f"{user.mention} shall get squogged!", files=[nextcord.File("./images/squogify.gif")])

    @commands.command(description="Kidnap someone", usage={"@user"})
    async def kidnap(self, ctx: nextcord.Message, user: nextcord.User):
        await ctx.reply(f"{user.mention} shall get kidnapped!", files=[nextcord.File(f"./images/Kidnap{random.randint(1, 2)}.jpg")])

    # Add something here later cuz im lazy raaahhh

def setup(bot):
    bot.add_cog(Fun(bot))