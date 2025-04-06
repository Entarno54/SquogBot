import os
import logging
import nextcord
import yt_dlp
import subprocess
from nextcord.ext import commands
import logging

SquogServer = 1356433463854497944
SquogToken = "MTM1NjU2MTY2MjQyOTM2ODQxMQ.G8aypc.CZBX-x6e4Oad3U5zO0nUgc02d9FDIDSNFybysI"

client = commands.Bot(command_prefix="!", intents=nextcord.Intents.all())
client.remove_command("help")

SquogMod = None

SquogFinalName: str = None
def SquogFilename(d):
    global SquogFinalName
    SquogFinalName = d.get('info_dict').get('_filename')

SquogVideo = {
    "verbose":True,
    "progress_hooks": [SquogFilename],
    'final_ext': 'mp3',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
    }],
    "outtmpl": './%(uploader)s_%(title)s.%(ext)s',
    "quality": "low"
}

SquogCurrentConnection: nextcord.VoiceClient = None

SquogDownload = yt_dlp.YoutubeDL(SquogVideo)

#    _____                                          _
#  / ____|                                        | |
# | |     ___  _ __ ___  _ __ ___   __ _ _ __   __| |___
# | |    / _ \| '_ ` _ \| '_ ` _ \ / _` | '_ \ / _` / __|
# | |___| (_) | | | | | | | | | | | (_| | | | | (_| \__ \
#  \_____\___/|_| |_| |_|_| |_| |_|\__,_|_| |_|\__,_|___/

@client.command()
async def help(ctx: nextcord.Message):
    embed = nextcord.Embed(title="Help")
    print(client.commands)
    for command in client.get_application_commands():
        print(command)

@client.command(description="Check how fast the bot will reply to you.", help="evil")
async def ping(ctx: nextcord.Message):
    await ctx.reply("Pong!")

@client.command(description="Join the voice channel.")
async def join(ctx: nextcord.Message):
    print("Joining")
    print(client.voice_clients)
    if client.voice_clients.__len__() == 0:
        if ctx.author.voice:
            global SquogCurrentConnection
            SquogCurrentConnection = await ctx.author.voice.channel.connect()
            await ctx.reply("Joined.")
        else:
            await ctx.reply("Can't join as you aren't in any voice channel.")
    else:
        await ctx.reply("Can't join as i'm already in a voice channel.")

@client.command(description="Leaves the voice channel.")
async def leave(ctx: nextcord.Message):
    print("Leaving")
    if client.voice_clients.__len__() != 0:
        await client.voice_clients[0].disconnect(force=True)
        await ctx.reply("Left.")
    else:
        await ctx.reply("Can't leave as i'm not in any voice channel.")

@client.command(description="Plays music in the voice channel.", usage={"link"})
async def play(ctx: nextcord.Message, link):
    global SquogEvilFilename
    global SquogFinalName
    SquogEvilFilename = None
    if client.voice_clients.__len__() == 0:
        return await ctx.reply("I'm not in a voice channel.")
    if client.voice_clients[0].is_playing():
        return await ctx.reply("I'm already playing music.")
    print(ctx.guild.voice_client.is_connected())
    print(SquogCurrentConnection)
    SquogVoiceClient = ctx.guild.voice_client
    print(link)
    SquogDownload.download(link)
    SquogInfo = SquogDownload.extract_info(link, download=False)
    SquogFinalName = SquogDownload.prepare_filename(SquogInfo)
    SquogLength = SquogFinalName.__len__() - 4
    SquogExt = os.path.splitext(SquogFinalName)
    print(SquogExt)
    SquogLength = SquogFinalName.find(SquogExt[1]) + 1
    print(SquogLength)
    SquogEvilFilename = f"{SquogFinalName[:SquogLength]}mp3"
    SquogVoiceClient.play(nextcord.FFmpegPCMAudio(f"{SquogEvilFilename}"))

@client.command(description="Stops the music in voice channel")
async def stop(ctx: nextcord.Message):
    if client.voice_clients.__len__() == 0:
        return await ctx.reply("I'm not in a voice channel.")
    if not SquogCurrentConnection.is_playing():
        return await ctx.reply("I'm not playing music.")
    SquogCurrentConnection.stop()

#  ______               _
# |  ____|             | |
# | |____   _____ _ __ | |_ ___
# |  __\ \ / / _ | '_ \| __/ __|
# | |___\ V |  __| | | | |_\__ \
# |______\_/ \___|_| |_|\__|___/

@client.event
async def on_member_join(member: nextcord.Member):
    print(f"Member {member.display_name} joined")
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
