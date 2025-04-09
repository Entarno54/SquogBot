import nextcord
from nextcord.ext import commands
import openai
import json

Enabled = True

SquogAILink = "https://api.webraft.in/v1"
SquogAIToken = "wr-tmkosxfStCjKSKsUJZueAS"

SquogAI = openai.OpenAI(api_key=SquogAIToken, base_url=SquogAILink)

SquogDataFile = open("./userinfo/userinfo.json", "r")
SquogData = json.loads(SquogDataFile.read())
SquogDataFile.close()

SquogUserPreset = {"id":  999, "messages":  [{"role": "system", "content": "You are a Squid Dog from game Changed. You are a white dog-looking creature made of latex, you have white squid tentacles with black paw beans, you have black eyes with white pupils, you have extra 2 arm paws. You must act like a curious creature and never say you are a PC program."}]}

async def getResponse(SquogMessageList):
    SquogResponse = SquogAI.chat.completions.create(messages=SquogMessageList, model="gpt-4o", temperature=0.9)
    return SquogResponse.json()

async def find(list: list, param: str, value: any):
    found = None
    for g in list:
        print(g)
        if g[param] == value:
            found = g
    return found

async def flush():
    SquogDataFile = open("./userinfo/userinfo.json", "w")
    SquogDataFile.write(json.dumps(SquogData))
    SquogDataFile.flush()
    SquogDataFile.close()

class AI(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot

    @commands.Cog.listener()
    async def on_message(self, message: nextcord.Message):

        if not Enabled:
            return

        SquogMention = False

        for Mention in message.mentions:
            if Mention.id == self.client.user.id:
                SquogMention = True

        if not SquogMention:
            return

        SquogUser = await find(SquogData, "id", message.author.id)

        if not SquogUser:
            SquogUser = SquogUserPreset.copy()
            SquogUser["id"] = message.author.id
            SquogUser["messages"] = []
            SquogData.append(SquogUser)

        SquogUser["messages"].append({"role": "user", "content": message.content})

        SquogResponse = await getResponse(SquogUser["messages"])
        print(SquogResponse)
        print(SquogResponse[0])
        SquogUser["messages"].append(SquogResponse["choices"][0]["message"])
        await message.reply(SquogResponse["choices"][0]["message"]["content"])

        await flush(SquogData)

def setup(bot):
    bot.add_cog(AI(bot))