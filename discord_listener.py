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
        discordmessage['type'] = 'message'
        jsonmessage = json.dumps(discordmessage)
        eventdata = (Message(jsonmessage))
        servicebusclient.send(eventdata)

@discordclient.event
async def on_raw_reaction_add(payload):
    if payload.user_id == 488839084245254167:
        return None #Bot doesn't care about reactions it issues
    
    discordmessage = {}
    discordmessage['type'] = 'reactionadd'
    discordmessage['channel_id'] = payload.channel_id
    discordmessage['guild_id'] = payload.guild_id
    discordmessage['message_id'] = payload.message_id
    discordmessage['emojiid'] = payload.emoji.id
    discordmessage['emojiname'] = payload.emoji.name
    jsonmessage = json.dumps(discordmessage)
    eventdata = (Message(jsonmessage))
    servicebusclient.send(eventdata)

@discordclient.event
async def on_raw_reaction_remove(payload):
    if payload.user_id == 488839084245254167:
        return None #Bot doesn't care about reactions it issues

    discordmessage = {}
    discordmessage['type'] = 'reactionremove'
    discordmessage['channel_id'] = payload.channel_id
    discordmessage['guild_id'] = payload.guild_id
    discordmessage['message_id'] = payload.message_id
    discordmessage['emojiid'] = payload.emoji.id
    discordmessage['emojiname'] = payload.emoji.name
    jsonmessage = json.dumps(discordmessage)
    eventdata = (Message(jsonmessage))
    servicebusclient.send(eventdata) 

discordclient.run(token)