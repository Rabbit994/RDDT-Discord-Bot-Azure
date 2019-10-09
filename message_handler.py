import json
from time import sleep
from azure.servicebus import QueueClient, Message
##Local Modules
import Modules.CosmosFramework as CosmosFramework
import Modules.CommonFramework as CommonFramework

#region Service Bus for incoming
config = CommonFramework.RetrieveConfigOptions('discordlisten')
connection_str = config['connectionstring']
queue = config['queue']
sbclient = QueueClient.from_connection_string(connection_str,queue)
#endregion
#region Service Bus for Outgoing
outboundeventhuboptions = CommonFramework.RetrieveConfigOptions('discordoutgoing')
outbound_connection_str = outboundeventhuboptions['connectionstring']
outbound_queue = outboundeventhuboptions['queue']
sboutboundclient = QueueClient.from_connection_string(outbound_connection_str,outbound_queue)
#endregion

errorcount = 0

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


with sbclient.get_receiver(prefetch=5) as queue_receiver:
    while True:
        try:
            messages = queue_receiver.fetch_next()
            for sbmessage in messages:
                body = str(sbmessage.message)
                body = json.loads(body)
                #print(body)
                if body['isadmin'] is True and body['botmention'] is True: #If the user is not admin, ignore
                    discordmessage = body['message'].split()
                    if discordmessage[1] == 'status':
                        messageembed = AdminFramework.status(body)
                        sboutboundclient.send(Message(create_channel_message_json(embed=messageembed,target=body['guildchannelid'])))
                    elif discordmessage[1] == 'ping':
                        message = AdminFramework.ping(body)
                        sboutboundclient.send(Message(create_channel_message_json(target=body['guildchannelid'],message=message)))
                    elif discordmessage[1] == 'channel':
                        message = AdminFramework.channel(body)
                        sboutboundclient.send(Message(create_channel_message_json(target=body['guildchannelid'],message=message)))
                    elif discordmessage[1] == 'locationadd':
                        message = AdminFramework.locationadd(body)
                        sboutboundclient.send(Message(create_channel_message_json(target=body['guildchannelid'],message=message)))
                    elif discordmessage[1] == 'locationremove':
                        message = AdminFramework.locationremove(body)
                        sboutboundclient.send(Message(create_channel_message_json(target=body['guildchannelid'],message=message)))
                    elif discordmessage[1] == 'severity':
                        message = AdminFramework.severity(body)
                        sboutboundclient.send(Message(create_channel_message_json(target=body['guildchannelid'],message=message)))
                    elif discordmessage[1] == 'help':
                        messageembed = AdminFramework.help(body)
                        sboutboundclient.send(Message(create_channel_message_json(target=body['guildchannelid'],embed=messageembed)))
                    elif discordmessage[1] == 'guildaddevent':
                        message = "Please Mention bot with word help to get started"
                        sboutboundclient.send(Message(create_channel_message_json(target=body['guildchannelid'],message=message)))
                sbmessage.complete()
        except:
            pass