import discord
from azure.servicebus import QueueClient, Message
import json
#Local Modules
import Modules.CommonFramework as CommonFramework
import Modules.DiscordFramework as DiscordFramework
import Modules.CosmosFramework as CosmosFramework

#import Modules.EventGridFramework as EventGridFramework
#import Modules.DiscordBotFramework as DiscordBotFramework

##Discord options
discordoptions = CommonFramework.RetrieveConfigOptions('discord')
token = discordoptions['token']
discordclient = discord.Client()
commandprefix = '!'

#Discord Incoming Service Bus setup
servicebusoptions = CommonFramework.RetrieveConfigOptions('discordlisten')
connection_str = servicebusoptions['connectionstring']
queue_path = servicebusoptions['queue']
servicebusclient = QueueClient.from_connection_string(connection_str,queue_path)
###

@discordclient.event
async def on_message(message):
    if message.author == discordclient.user:
        return None #Bot ignores itself
    
    if message.guild is None or message.content.startswith(commandprefix): #Adding support for Private Message
        discordmessage = {}
        discordmessage['authorid'] = message.author.id 
        discordmessage['authordisplayname'] = message.author.display_name
        discordmessage['authormention'] = message.author.mention
        if discordclient.user in message.mentions:
            discordmessage['botmention'] = True
        if message.guild is not None:
            discordmessage['guildid'] = message.guild.id
            discordmessage['guildchannelid'] = message.channel.id
            discordmessage['guildchannelname'] = message.channel.name
            discordmessage['guildchannelmention'] = message.channel.mention
            discordmessage['admin'] = message.author.guild_permissions.administrator
            discordmessage['kick_members'] = message.author.guild_permissions.kick_members
            discordmessage['ban_members'] = message.author.guild_permissions.ban_members
        else:
            discordmessage['privatemessage'] = True
            discordmessage['privatemessagechannelid'] = message.channel.id
        discordmessage['message'] = message.content
        jsonmessage = json.dumps(discordmessage)
        eventdata = (Message(jsonmessage))
        servicebusclient.send(eventdata)

discordclient.run(token)