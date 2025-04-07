import nextcord
from nextcord.ext import commands
import os

#Defining the basic stuff here
SquogServer = 1356433463854497944
SquogToken = "MTM1NjU2MTY2MjQyOTM2ODQxMQ.G8aypc.CZBX-x6e4Oad3U5zO0nUgc02d9FDIDSNFybysI"

client = commands.Bot(command_prefix="!", intents=nextcord.Intents.all())
#Removing the default help command because no
client.remove_command("help")

#Loading Cogs
for filename in os.listdir('./commands'):
    if filename.endswith('.py'):
        client.load_extension(f'commands.{filename[:-3]}')

for filename in os.listdir("./events"):
    if filename.endswith('.py'):
        client.load_extension(f'events.{filename[:-3]}')

# Starting bot
client.run(SquogToken)
