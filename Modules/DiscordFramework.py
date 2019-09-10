import json
import requests
import os
from time import sleep
import Modules.CommonFramework as CommonFramework

baseuri = "https://discordapp.com/api/v6"
config = CommonFramework.RetrieveConfigOptions("discord")


##Private Functions
def GetDiscordHeaders():
    """Generates Header for Discord HTTP requests"""
    global config
    header = {'Authorization': str('Bot ' + config['token']), 'User-Agent': '/r/worldoftanks Discord Bot (https://github.com/Rabbit994/RDDT-Discord-Bot-Azure-PyFunc, v0.0.1)'}
    return header

def __status_code_check(headers:dict, status_code:int) -> None:
    if status_code == 429:
        sleep(int(headers['X-RateLimit-Reset-After'])) #If we exceed request limit, go ahead and sleep
    return None

def SendDiscordGetRequest(uri):
    """Sends Discord Get request and returns JSON body"""
    r = requests.get(uri, headers=GetDiscordHeaders())
    __status_code_check(r.headers, r.status_code)
    data = r.json()
    return data

def SendDiscordPutRequest(uri):
    """Issues put request and returns status code"""
    r = requests.put(uri, headers=GetDiscordHeaders())
    __status_code_check(r.headers, r.status_code)
    data = r.status_code
    return data

def SendDiscordDeleteRequest(uri):
    """Issues Delete request and returns status code"""
    r = requests.delete(uri, headers=GetDiscordHeaders())
    __status_code_check(r.headers, r.status_code)
    data = r.status_code
    return data

def SendDiscordPostRequest(uri,body):
    """Issues a Post request and returns status code"""
    r = requests.post(uri, json=body, headers=GetDiscordHeaders())
    __status_code_check(r.headers, r.status_code)
    if r.text == '':
        return None
    data = r.json()
    return data

##Module Functions
def GetUserRoles(uid,DiscordServerID):
    """Get Users Roles in JSON from API and returns list"""
    global baseuri
    uri = "{0}/guilds/{1}/members/{2}".format(baseuri,DiscordServerID,uid)
    data = SendDiscordGetRequest(uri)
    lstroles = []
    if 'message' in data:
        if data['message'] == "Unknown Member":
            lstroles = 0
            return lstroles
    for r in data['roles']:
        lstroles.append(int(r))
    return lstroles

def AddUserRole(roleid,discordid,DiscordServerID):
    """Adds respective role ID to discord ID in question and returns status code"""
    global baseuri
    uri = "{0}/guilds/{1}/members/{2}/roles/{3}".format(baseuri,DiscordServerID,discordid,roleid)
    data = SendDiscordPutRequest(uri)
    return data

def RemoveUserRole(roleid,discordid,DiscordServerID):
    """Removes respective role ID to Discord ID in question and returns status code"""
    global baseuri
    uri = "{0}/guilds/{1}/members/{2}/roles/{3}".format(baseuri,DiscordServerID,discordid,roleid)
    data = SendDiscordDeleteRequest(uri)
    return data

def GetAllChannels(DiscordServerID):
    """Gets all the channels"""
    global baseuri
    uri = "{0}/guilds/{1}/channels".format(baseuri,DiscordServerID)
    data = SendDiscordGetRequest(uri)
    return data

def SendDiscordMessage(message:str,channelid:str,embed:dict=None) -> dict:
    """Sends Discord message to Channel specific ID"""
    global baseuri
    uri = "{0}/channels/{1}/messages".format(baseuri,channelid)
    omessage = {}
    if message is not None:
        omessage['content'] = message
        omessage['tts'] = False
    if embed is not None:
        omessage['embed'] = embed
    data = SendDiscordPostRequest(uri,omessage)
    return data

def send_discord_private_message(message,discordid):
    """Send Private Discord message to Discord ID"""
    global baseuri
    uri = "{0}/users/@me/channels".format(baseuri)
    body = {}
    body['recipient_id'] = discordid
    data = SendDiscordPostRequest(uri,body)
    SendDiscordMessage(message,data['id'])

def get_channel_info(channelid:str) -> dict:
    global baseuri
    uri = "{0}/channels/{1}".format(baseuri,channelid)
    data = SendDiscordGetRequest(uri)
    return data

def send_typing_indicator(channelid:str) -> None:
    """Send Typing Indicator to channel in question"""
    global baseuri
    uri = "{0}/channels/{1}/typing".format(baseuri,channelid)
    SendDiscordPostRequest(uri,body=None)
    return None
    