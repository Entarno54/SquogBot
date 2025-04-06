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

for filename in os.listdir("./events"):
    if filename.endswith('.py'):
        client.load_extension(f'events.{filename[:-3]}')

#   ______                     _   _
#  |  ____|                   | | (_)
#  | |__  __  _____  ___ _   _| |_ _ _ __   __ _
#  |  __| \ \/ / _ \/ __| | | | __| | '_ \ / _` |
#  | |____ >  |  __| (__| |_| | |_| | | | | (_| |
#  |______/_/\_\___|\___|\__,_|\__|_|_| |_|\__, |
#                                           __/ |
#                                          |___/
client.run(SquogToken)
