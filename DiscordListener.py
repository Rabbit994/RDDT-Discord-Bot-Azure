import discord
import Frameworks.CommonFramework as CommonFramework
import Frameworks.EventGridFramework as EventGridFramework

discordoptions = CommonFramework.RetrieveConfigOptions('discord')
token = discordoptions['token']
commandprefix = '?'
client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return #Bot ignores itself
    
    if message.content.startswith(commandprefix):
        eventid=str(message.id)
        subject="message"
        data = dict()
        if message.guild is None:
            data['privatemessage'] = True
        else:
            data['channelid'] = message.channel.id
            data['channelname'] = message.channel.name
        data['authorid'] = message.author.id
        data['message'] = message.content
        eventtype = message.content
        eventtype = eventtype.split()
        eventtype = eventtype[0]
        EventGridFramework.publish_event(eventid,subject,data,eventtype)

client.run(token)