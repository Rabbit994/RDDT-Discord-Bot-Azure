import discord
import Frameworks.CommonFramework as CommonFramework
import Frameworks.EventGridFramework as EventGridFramework
import Frameworks.DiscordBotFramework as DiscordBotFramework


discordoptions = CommonFramework.RetrieveConfigOptions('discord')
token = discordoptions['token']
commandprefix = '?'
client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return #Bot ignores itself
    
    if message.content.startswith(commandprefix):
        if message.content.startswith("?register"):
            pass
        elif message.content.startswith("?info"):
            pass
        

client.run(token)