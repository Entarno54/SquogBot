import nextcord
from nextcord.ext import commands
import os

SquogServer = 1356433463854497944
SquogToken = "MTM1NjU2MTY2MjQyOTM2ODQxMQ.G8aypc.CZBX-x6e4Oad3U5zO0nUgc02d9FDIDSNFybysI"

client = commands.Bot(command_prefix="!", intents=nextcord.Intents.all())
client.remove_command("help")

SquogMod = None

for filename in os.listdir('./commands'):
    if filename.endswith('.py'):
        client.load_extension(f'commands.{filename[:-3]}')


#  ______               _
# |  ____|             | |
# | |____   _____ _ __ | |_ ___
# |  __\ \ / / _ | '_ \| __/ __|
# | |___\ V |  __| | | | |_\__ \
# |______\_/ \___|_| |_|\__|___/

@client.event
async def on_member_join(member: nextcord.Member):
    print(f"Member {member.display_name} joined")
    if member.guild.id == 1356433463854497944:  # Only for the squog server
        await member.add_roles(nextcord.utils.get(member.guild.roles, name="Squog"))

@client.event
async def on_member_remove(member: nextcord.Member):
    print(f"Member {member.display_name} left")

@client.event
async def on_message_delete(msg: nextcord.Message):
    embed = nextcord.Embed(
        title = "Message delete",
        description = msg.content
    )
    embed.set_author(name = msg.author.name)
    for image in msg.attachments:
        embed.set_image(image.url) # Unfortunately i cant add multiple images.
    await SquogMod.send(embed=embed)

@client.event
async def on_command(ctx: commands.Context):
    embed = nextcord.Embed(
        title="Command used",
        description=ctx.message.content
    )
    field = embed.add_field(name="Channel", value = ctx.channel.name)
    await SquogMod.send(embed=embed)

@client.event
async def on_ready():
    global SquogMod
    print("Bot logged")
    SquogMod = client.get_channel(1356577069068324986)
    print(SquogMod)

#   ______                     _   _
#  |  ____|                   | | (_)
#  | |__  __  _____  ___ _   _| |_ _ _ __   __ _
#  |  __| \ \/ / _ \/ __| | | | __| | '_ \ / _` |
#  | |____ >  |  __| (__| |_| | |_| | | | | (_| |
#  |______/_/\_\___|\___|\__,_|\__|_|_| |_|\__, |
#                                           __/ |
#                                          |___/
client.run(SquogToken)
