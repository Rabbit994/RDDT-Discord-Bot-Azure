#This handles incoming discord messages

import json
from time import sleep
import requests
##3rd Party Modules
from azure.servicebus import QueueClient, Message
##Local Modules
import Modules.CosmosFramework as CosmosFramework
import Modules.CommonFramework as CommonFramework
import Modules.DiscordFramework as DiscordFramework
import Modules.DiscordBotFramework as DiscordBotFramework

#region Service Bus for incoming
config = CommonFramework.RetrieveConfigOptions('discordlisten')
connection_str = config['connectionstring']
queue = config['queue']
sbclient = QueueClient.from_connection_string(connection_str,queue)
#endregion

#region Unused (?)
def create_channel_message_json(target:str,message:str=None,embed:dict=None) -> str:
    returnmessage = {}
    returnmessage['privatemessage'] = False
    returnmessage['targetid'] = str(target)
    if message is not None:
        returnmessage['content'] = message
    else:
        returnmessage['content'] = None
    if embed is not None:
        returnmessage['embed'] = embed
    else:
        returnmessage['embed'] = None
    returnmessagejson = json.dumps(returnmessage)
    return returnmessagejson
#endregion

def __return_message(body:dict, returnmessage:dict) -> None:
    """Gets original message and return message and sends to proper channels"""
    if 'channel' in returnmessage:
        DiscordFramework.SendDiscordMessage(returnmessage['channel'],body['guildchannelid'])
    if 'author' in returnmessage:
        DiscordFramework.send_discord_private_message(returnmessage['author'],body['authorid'])
    return None

with sbclient.get_receiver(prefetch=5) as queue_receiver:
    while True:
        try:
            messages = queue_receiver.fetch_next()
            for sbmessage in messages:
                body = str(sbmessage.message)
                body = json.loads(body)
                discordmessage = body['message'].split()
                #print(body)
                if discordmessage[0] == '!register':
                    returnmessage = DiscordBotFramework.register(body)
                    if 'privatemessage' in body:
                        del returnmessage['channel']
                    __return_message(body,returnmessage)
                
                elif discordmessage[0] == '!cw':
                    if body['guildchannelid'] == 508848701058318366: #RDDT
                        data = CommonFramework.GetClanBattles(1000001505)
                        webhooks = CommonFramework.RetrieveConfigOptions('webhooks')
                        requests.post(webhooks['rddt'], data=data)
                    elif body['guildchannelid'] == 508849107855474688: #TL-DR
                        data = CommonFramework.GetClanBattles(1000003392)
                        webhooks = CommonFramework.RetrieveConfigOptions('webhooks')
                        requests.post(webhooks['tl-dr'], data=data)
                
                elif discordmessage[0] == '!update':
                    if body['guildchannelid'] == 506659095521132554:
                        returnmessage = DiscordBotFramework.update(body)
                        __return_message(body,returnmessage)
                
                elif discordmessage[0] == '!status':
                    returnmessage = DiscordBotFramework.status(body)
                elif discordmessage[0] == '!cone':
                    pass
                elif discordmessage[0] == '!ping':
                    pass

                sbmessage.complete()
        except:
            pass