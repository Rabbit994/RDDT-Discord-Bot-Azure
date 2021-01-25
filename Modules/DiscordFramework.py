import json
import requests
import os
from time import sleep
import Modules.CommonFramework as CommonFramework
baseuri = "https://discord.com/api"
config = CommonFramework.RetrieveConfigOptions("discord")


class DiscordHTTP:
    def __init__(self) -> None:
        global config
        self.token = config['token']
        self.baseuri = "https://discord.com/api"

    def __generate_discord_header(self) -> dict:
        header = {'Authorization': str(f"Bot {self.token}"), 'User-Agent': '/r/worldoftanks Discord Bot (https://github.com/Rabbit994/RDDT-Discord-Bot-Azure, v1.0.5)'}
        return header
    
    def __send_discord_put_request(self, uri:str):
        statuscode = 0
        for x in range(0,3):
            r = requests.put(uri, headers=self.__generate_discord_header())
            statuscode = r.status_code
            if statuscode == 429: #If 
                sleep(int(r.headers['X-RateLimit-Reset-After']))
            elif statuscode in range(200,299):
                return r
        return r #Return r which will be HTTP error
    
    def __send_discord_delete_request(self, uri:str):
        for x in range(0,3):
            r = requests.delete(url=uri, headers=self.__generate_discord_header())
            statuscode = r.status_code
            if statuscode == 429:
                sleep(int(r.headers['X-RateLimit-Reset-After']))
            elif statuscode in range(200,299):
                return r
        return r

    def __send_discord_post_request(self, uri:str, body:dict):
        for x in range(0,3):
            r = requests.post(url=uri, json=body, headers=self.__generate_discord_header())
            statuscode = r.status_code
            if statuscode == 429:
                sleep(int(r.headers['X-RateLimit-Reset-After']))
            elif statuscode in range(200,299):
                return r
        return r

    def add_reaction_to_message(self, channelid:int, messageid:int, emoji:str) -> int:
        """Adds reaction to message, pass str of emoji id, will return status code"""
        if channelid is None or messageid is None or emoji is None:
            return None
        emoji = emoji.replace(":","%3A")
        emoji = emoji.replace("+","%2B")
        uri = f"{self.baseuri}/channels/{channelid}/messages/{messageid}/reactions/{emoji}/@me"
        response = self.__send_discord_put_request(uri=uri)
        return response.status_code
    
    def add_role_to_user(self,guildid:int,userid:int,roleid:int):
        uri = f"{self.baseuri}/guilds/{guildid}/members/{userid}/roles/{roleid}"
        response = self.__send_discord_put_request(uri)
        if response.status_code != 204: #send it again
            sleep(5)
            response = self.__send_discord_put_request(uri)
        return response.status_code

    def remove_role_from_user(self,guildid:int,userid:int,roleid:int):
        uri = f"{self.baseuri}/guilds/{guildid}/members/{userid}/roles/{roleid}"
        response = self.__send_discord_delete_request(uri)
        if response.status_code != 204: #send it again
            sleep(5)
            response = self.__send_discord_delete_request(uri)
        return response.status_code

    def post_message(self,message:str, channelid:int, embed:dict = None):
        #Post message
        uri = f"{self.baseuri}/channels/{channelid}/messages"
        
        pass
##Private Functions
def GetDiscordHeaders():
    """Generates Header for Discord HTTP requests"""
    global config
    header = {'Authorization': str('Bot ' + config['token']), 'User-Agent': '/r/worldoftanks Discord Bot (https://github.com/Rabbit994/RDDT-Discord-Bot-Azure, v0.0.1)'}
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
def GetUserRoles(uid:str,DiscordServerID:str) -> list:
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
    messagedata = SendDiscordMessage(message,data['id'])
    return messagedata

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

def get_member_list(guildid:str,after:str=None,limit:int=1000) -> dict:
    """Get Member list of Server(Guild) in question"""
    global baseuri
    uri = "{0}/guilds/{1}/members?limit={2}".format(baseuri,guildid,limit)
    if after is not None:
        uri += "&after={0}".format(after)
    returndata = SendDiscordGetRequest(uri)
    return returndata

def get_user_info(discordid:str) -> dict:
    """Gets global user information"""
    global baseuri
    uri = "{0}/users/{1}".format(baseuri,discordid)
    returndata = SendDiscordGetRequest(uri)
    return returndata

def get_user_guild_info(discordid:str,guildid:str) -> dict:
    """Gets guild user data"""
    global baseuri
    uri = "{0}/guilds/{1}/members/{2}".format(baseuri,guildid,discordid)
    returndata = SendDiscordGetRequest(uri)
    return returndata

def delete_message(messageid:str,channelid:str) -> None:
    """Deletes messaage"""
    global baseuri
    uri = f"{baseuri}/channels/{channelid}/messages/{messageid}"
    returndata = SendDiscordDeleteRequest(uri)
    return returndata   