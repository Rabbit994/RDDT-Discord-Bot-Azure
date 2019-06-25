import json
import requests
import os
import Frameworks.CommonFramework as CommonFramework

baseuri = "https://discordapp.com/api/v6"
config = CommonFramework.RetrieveConfigOptions("discord")

def GetDiscordHeaders():
    """Generates Header for Discord HTTP requests"""
    global config
    header = {'Authorization': str('Bot ' + config['token']), 'User-Agent': '/r/worldoftanks Discord Bot (https://github.com/Rabbit994/RDDT-Discord-Bot-Azure-PyFunc, v0.0.1)'}
    return header

def SendDiscordGetRequest(uri):
    """Sends Discord Get request and returns JSON body"""
    r = requests.get(uri, headers=GetDiscordHeaders())
    data = r.json()
    return data

def SendDiscordPutRequest(uri):
    """Issues put request and returns status code"""
    r = requests.put(uri, headers=GetDiscordHeaders())
    data = r.status_code
    return data

def SendDiscordDeleteRequest(uri):
    """Issues Delete request and returns status code"""
    r = requests.delete(uri, headers=GetDiscordHeaders())
    data = r.status_code
    return data

def SendDiscordPostRequest(uri,body):
    """Issues a Post request and returns status code"""
    r = requests.post(uri, json=body, headers=GetDiscordHeaders())
    data = r.json()
    return data

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

def SendDiscordMessage(message,channelid):
    """Sends Discord message to Channel specific ID"""
    global baseuri
    uri = "{0}/channels/{1}/messages".format(baseuri,channelid)
    message = {"content": message}
    message['tts'] = False
    data = SendDiscordPostRequest(uri,message)
    return data

def send_discord_private_message(discordid,message):
    """Send Private Discord message to Discord ID"""
    global baseuri
    uri = "{0}/users/@me/channels".format(baseuri)
    body = dict()
    body['recipient_id'] = discordid
    data = SendDiscordPostRequest(uri,body)
    SendDiscordMessage(message,data['id'])
    