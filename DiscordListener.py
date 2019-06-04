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
        try:
            eventid = str(message.id)
            eventtype = "message"

            data = dict()
            if message.guild is None:
                data['privatemessage'] = True
            else:
                data['channelid'] = str(message.channel.id)
                data['channelname'] = str(message.channel.name)
            data['serverid'] = str(message.guild.id)
            data['authorid'] = str(message.author.id)
            data['message'] = str(message.content)
            subject = message.content
            subject = subject.split()
            subject = subject[0]
            await EventGridFramework.publish_event(eventid,subject,data,eventtype)
        except Exception as e:
            print(e) #Print and move on

client.run(token)