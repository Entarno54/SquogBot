import nextcord
from nextcord.ext import commands
import yt_dlp
import os
import threading

SquogFinalName: str = None
SquogPlaying = {

}

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
            SquogPlaying[ctx.guild.id] = False
        else:
            await ctx.reply("Can't leave as i'm not in any voice channel.")

    @commands.command(description="Plays music in the voice channel.", usage={"link"})
    async def play(self, ctx: nextcord.Message, link, loop: bool | None):
        if not ctx.guild.voice_client:
            return await ctx.reply("I'm not in a voice channel.")
        if ctx.guild.voice_client.is_playing():
            return await ctx.reply("I'm already playing music.")
        # Extracting info for the filename
        if loop:
            SquogPlaying[ctx.guild.id] = True

        SquogInfo = SquogDownload.extract_info(link, download=False)

        Embed = nextcord.Embed(title="Loading music", description=SquogDownload.prepare_filename(SquogInfo))

        # Notifying the user that music is getting started so they know its there
        await ctx.reply(embed=Embed)

        SquogVoiceClient = ctx.guild.voice_client

        # Function i will pass to the thread
        def Process():
            #Downloading the music
            SquogDownload.download(link)
            #Getting the filename again
            SquogFinalName = SquogDownload.prepare_filename(SquogInfo)
            #Getting the file extension (webp, mp4)
            SquogExt = os.path.splitext(SquogFinalName)
            #Finding the file length without the extension
            SquogLength = SquogFinalName.find(SquogExt[1]) + 1
            #Convering the extension to mp3 because
            #yt-dlp returns the original filename instead of the converted one
            SquogEvilFilename = f"{SquogFinalName[:SquogLength]}mp3"

            #Starting the music

            if SquogPlaying[ctx.guild.id] == True:
                while SquogPlaying[ctx.guild.id] == True:
                    SquogVoiceClient.play(nextcord.FFmpegPCMAudio(f"{SquogEvilFilename}"))
            else:
                SquogPlaying[ctx.guild.id] == True


        # I've to start this in a different thread because of how long some videos take to load...
        threading.Thread(target=Process).start()

    @commands.command(description="Stops the music in voice channel")
    async def stop(self, ctx: nextcord.Message):
        if not ctx.guild.voice_client:
            return await ctx.reply("I'm not in a voice channel.")
        if not ctx.guild.voice_client.is_playing():
            return await ctx.reply("I'm not playing music.")
        ctx.guild.voice_client.stop()
        SquogPlaying[ctx.guild.id] = False

def setup(bot):
    bot.add_cog(Voice(bot))