import nextcord
from nextcord.ext import commands

class Members(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: nextcord.Member):
        print(f"Member {member.display_name} joined")
        if member.guild.id == 1356433463854497944:  # Only for the squog server
            await member.add_roles(nextcord.utils.get(member.guild.roles, name="Squog"))

    @commands.Cog.listener()
    async def on_member_remove(self, member: nextcord.Member):
        print(f"Member {member.display_name} left")

def setup(bot):
    bot.add_cog(Members(bot))