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

def __return_message(body:dict, returnmessage:dict) -> None:
    """Gets original message and return message and sends to proper channels"""
    if 'channel' in returnmessage:
        DiscordFramework.SendDiscordMessage(returnmessage['channel'],body['guildchannelid'])
    if 'author' in returnmessage:
        DiscordFramework.send_discord_private_message(returnmessage['author'],body['authorid'])
    if 'target' in returnmessage and 'targetdiscordid' in returnmessage:
        DiscordFramework.send_discord_private_message(returnmessage['target'],returnmessage['targetdiscordid'])
    return None

with sbclient.get_receiver(prefetch=5) as queue_receiver:
    while True:
        try:
            messages = queue_receiver.fetch_next()
            for sbmessage in messages:
                body = str(sbmessage.message)
                body = json.loads(body)
                if body['type'] == 'message':
                    discordmessage = body['message'].split()
                    #print(body)
                    if discordmessage[0] == '!register' and (
                    body['guildchannelid'] == 507725600073449482 or body.get("privatemessage") is True):
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
                        elif body['guildchannelid'] == 509529887988645892: #RDTT2
                            data = CommonFramework.GetClanBattles(1000002659)
                            webhooks = CommonFramework.RetrieveConfigOptions('webhooks')
                            requests.post(webhooks['rdtt2'], data=data)
                        elif body['guildchannelid'] == 713854191784820827: #RDDT6
                            data = CommonFramework.GetClanBattles(1000005754)
                            webhooks = CommonFramework.RetrieveConfigOptions('webhooks')
                            requests.post(webhooks['rddt6'], data=data)

                    elif discordmessage[0] == '!update':
                        if body['guildchannelid'] == 506659095521132554:
                            returnmessage = DiscordBotFramework.update(body)
                            __return_message(body,returnmessage)

                    elif discordmessage[0] == '!status':
                        returnmessage = DiscordBotFramework.status(body)
                        __return_message(body,returnmessage)

                    elif discordmessage[0] == '!cone':
                        if body['kick_members'] is True:
                            returnmessage = DiscordBotFramework.cone(body)
                            __return_message(body,returnmessage)

                    elif discordmessage[0] == '!ping':
                        returnmessage = {'channel':'pong!'}
                        __return_message(body,returnmessage)
                        
                    elif discordmessage[0] == '!citadel':
                        returnmessage = DiscordBotFramework.citadel(body)
                        __return_message(body,returnmessage)

                    elif discordmessage[0] == '!startcontest':
                        returnmessage = DiscordBotFramework.startcontest(body)
                        __return_message(body,returnmessage)

                    elif discordmessage[0] == '!addgame':
                        pass

                    elif "http" in body['message'].lower():
                        returnmessage = DiscordBotFramework.handle_links(body)
                        if returnmessage:
                            __return_message(body,returnmessage)
                        
                elif body['type'] == 'reactionadd':
                    pass #Future actions
                elif body['type'] == 'reactionremove':
                    pass #Future actions
                sbmessage.complete()
                
        except Exception as e:
            DiscordFramework.SendDiscordMessage(str(e),'491800495980150789')
            sbmessage.abandon() #If message fails, abandon it so it can be reprocessed quickly
            pass
