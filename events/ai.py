import os
from pyexpat.errors import messages

import nextcord
from nextcord.ext import commands
import requests
import json

SquogAILink = "https://api.webraft.in/v2/chat/completions"
SquogAIToken = "wr-tmkosxfStCjKSKsUJZueAS"

SquogDataFile = open("./userinfo/userinfo.json", "rw")
SquogData = json.loads(SquogDataFile.read())

SquogUserPreset = {"id":  999, "messages":  []}

async def getResponse(SquogMessageList):
    return requests.post(SquogAILink, headers={"Authorization": f"Bearer {SquogAIToken}"}, body={"model": "gpt-4o", messages:messages}).json()

async def find(list: list, param: str, value: any):
    found = None
    for g in list:
        print(g)
        if g[param] == value:
            found = g
    return found

async def flush(data):
    SquogDataFile.write(json.dumps(SquogData))
    SquogDataFile.flush()

class AI(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot

    @commands.Cog.listener()
    async def on_message(self, message: nextcord.Message):
        print(message.content)
        self.client.process_application_commands(message)

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

        Response = getResponse(SquogUser["messages"])

        SquogUser["messages"].append(Response["choices"][0]["message"])

        await message.reply(Response["choices"][0]["message"]["content"])

        await flush(SquogData)

def setup(bot):
    bot.add_cog(AI(bot))