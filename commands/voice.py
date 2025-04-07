import nextcord
from nextcord.ext import commands
import yt_dlp
import os
import multiprocessing

SquogFinalName: str = None

SquogVideo = {
    "verbose": True,
    'final_ext': 'mp3',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
    }],
    "outtmpl": './music/%(uploader)s_%(title)s.%(ext)s',
    "quality": "low"
}

SquogCurrentConnection: nextcord.VoiceClient = None

SquogDownload = yt_dlp.YoutubeDL(SquogVideo)

class Voice(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command(description="Join the voice channel.")
    async def join(self, ctx: nextcord.Message):
        print("Joining")
        if not ctx.guild.voice_client:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
                await ctx.reply("Joined.")
            else:
                await ctx.reply("Can't join as you aren't in any voice channel.")
        else:
            await ctx.reply("Can't join as i'm already in a voice channel.")

    @commands.command(description="Leaves the voice channel.")
    async def leave(self, ctx: nextcord.Message):
        print("Leaving")
        if ctx.guild.voice_client:
            await ctx.guild.voice_client.disconnect(force=True)
            await ctx.reply("Left.")
        else:
            await ctx.reply("Can't leave as i'm not in any voice channel.")

    @commands.command(description="Plays music in the voice channel.", usage={"link"})
    async def play(self, ctx: nextcord.Message, link):
        global SquogEvilFilename
        global SquogFinalName
        SquogEvilFilename = None
        if not ctx.guild.voice_client:
            return await ctx.reply("I'm not in a voice channel.")
        if ctx.guild.voice_client.is_playing():
            return await ctx.reply("I'm already playing music.")
        # Extracting info for the filename
        SquogInfo = SquogDownload.extract_info(link, download=False)
        Embed = nextcord.Embed(title="Loading music", description=SquogDownload.prepare_filename(SquogInfo))
        # Notifying the user that music is getting started so they know its there
        await ctx.reply(embed=Embed)

        SquogVoiceClient = ctx.guild.voice_client

        def Test():
            SquogDownload.download(link)
            SquogFinalName = SquogDownload.prepare_filename(SquogInfo)
            SquogLength = SquogFinalName.__len__() - 4
            SquogExt = os.path.splitext(SquogFinalName)
            print(SquogExt)
            SquogLength = SquogFinalName.find(SquogExt[1]) + 1
            print(SquogLength)
            SquogEvilFilename = f"{SquogFinalName[:SquogLength]}mp3"
            SquogVoiceClient.play(nextcord.FFmpegPCMAudio(f"{SquogEvilFilename}"))

        multiprocessing.Process(target=Test).start()

    @commands.command(description="Stops the music in voice channel")
    async def stop(self, ctx: nextcord.Message):
        if not ctx.guild.voice_client:
            return await ctx.reply("I'm not in a voice channel.")
        if not ctx.guild.voice_client.is_playing():
            return await ctx.reply("I'm not playing music.")
        ctx.guild.voice_client.stop()

def setup(bot):
    bot.add_cog(Voice(bot))