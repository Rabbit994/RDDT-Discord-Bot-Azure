import discord
import Modules.CommonFramework as CommonFramework
#import Modules.EventGridFramework as EventGridFramework
import Modules.DiscordBotFramework as DiscordBotFramework
import Modules.DiscordFramework as DiscordFramework


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
            returnmessage = await DiscordBotFramework.register(message)
            if 'channel' in returnmessage:
                DiscordFramework.SendDiscordMessage(returnmessage['channel'],message.channel.id)
            if 'author' in returnmessage:
                DiscordFramework.send_discord_private_message(returnmessage['author'],message.author.id)  
        elif message.content.startswith("?info"):
            pass
        elif message.content.startswith("?parse"):
            pass

         
    
client.run(token)