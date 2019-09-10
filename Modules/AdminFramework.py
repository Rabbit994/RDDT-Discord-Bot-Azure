import json

import Modules.CommonFramework as CommonFramework
import Modules.CosmosFramework as CosmosFramework
import Modules.DiscordFramework as DiscordFramework
container = 'server' #CosmosDB Container for servers

def __get_server_info(guildid:str) -> dict:
    """Gets Server info"""
    global container
    result = CosmosFramework.QueryItems('SELECT * FROM c WHERE c.discordid ="{0}"'.format(guildid),container=container)
    return result[0]

def status(body:dict) -> dict:
    result = __get_server_info(body['guildid'])
    embed = {}
    embedfields = []
    embedfield = {}
    embed['title'] = "Server Status"
    embedfield['name'] = "Severity"
    embedfield['value'] = result['severity']
    embedfields.append(dict(embedfield)) #So telling python to load dictionary
    embedfield['name'] = "Everyone Ping"
    if result['ping'] is True:
        embedfield['value'] = "Enabled"
    else:
        embedfield['value'] = "Disabled"
    embedfields.append(dict(embedfield))
    embedfield['name'] = "Channel"
    channelinfo = DiscordFramework.get_channel_info(result['channelid'])
    embedfield['value'] = "#{0}".format(channelinfo['name'])
    embedfields.append(dict(embedfield))
    embedfield['name'] = "Locations"
    locations = str()
    if 'geocodes' not in result or not result['geocodes']:
        embedfield['value'] = "No Locations set"
    else:
        for geo in result['geocodes']:
            georesult = CosmosFramework.QueryItems('SELECT c.name,c.state FROM c WHERE c.id="{0}"'.format(geo),container='zone')
            georesult = georesult[0]
            locations += "{0}, {1} \n".format(georesult['name'],georesult['state'])
        embedfield['value'] = locations
    embedfields.append(dict(embedfield))
    embed['fields'] = embedfields
    return embed
    
def ping(body:dict) -> str:
    result = __get_server_info(body['guildid'])
    if result['ping'] is True:
        result['ping'] = False
        message = "@ everyone has been disabled for all alerts"
    elif result['ping'] is False:
        result['ping'] = True
        message = "@ everyone has been enabled for all alerts, check alert severity level if you don't want everyone to flip out over pings"
    else:
        message = "Error Occurred during processing"
    CosmosFramework.ReplaceItem(result['_self'],result)
    return message

def channel(body:dict) -> str:
    result = __get_server_info(body['guildid'])
    message = body['message']
    try:
        message = message.split()
        channel = message[2].replace('<','')
        channel = channel.replace('#', '')
        channel = channel.replace('>', '')
        channel = int(channel) #If channel isn't int, TypeError out
        result['channelid'] = str(channel) #Channels are stored in Database as str
        CosmosFramework.ReplaceItem(result['_self'],result)
        channelinfo = DiscordFramework.get_channel_info(channel)
        returnmessage = 'Alert channel changed to #{0}'.format(channelinfo['name'])
    except:
        returnmessage = 'Please mention the channel you wish to send alerts to'
    return returnmessage

def locationadd(body:dict) -> str:
    serverresult = __get_server_info(body['guildid'])
    message = body['message']
    returnmessage = str()
    try:
        message = message.split()
        if 'geocodes' not in serverresult:
            zonelist = []
        else:
            zonelist = serverresult['geocodes']
        zonequery = 'SELECT * FROM c WHERE ARRAY_CONTAINS(c.zipcodes, "{0}", true)'.format(message[2])
        zoneresult = CosmosFramework.QueryItems(cosmosdbquery=zonequery,container='zone')
        if zoneresult: #Meaning zipcode found
            if zoneresult[0]['id'] not in zonelist:
                zonelist.append(zoneresult[0]['id'])
                returnmessage += 'Weather Zone: {0} added to server for County: **{1}** State: **{2}** \n'.format(zoneresult[0]['id'],zoneresult[0]['name'],zoneresult[0]['state'])
            else:
                returnmessage += 'Area already added for server, locations are stored at county level.'
        else:
            returnmessage = "Weather Zone not found for this zip code, try nearby zip code. Alerts are done at County level"
        serverresult['geocodes'] = zonelist
        CosmosFramework.ReplaceItem(serverresult['_self'],serverresult)
    except:
        returnmessage = "Error occurred while adding Zone to server"
    finally:
        return returnmessage

def locationremove(body:dict) -> str:
    serverresult = __get_server_info(body['guildid'])
    message = body['message']
    returnmessage = str()
    try:
        message = message.split()
        if 'geocodes' not in serverresult:
            returnmessage = "Server does not have any locations to remove"
            return returnmessage
        else:
            zonelist = serverresult['geocodes']
        zonequery = 'SELECT * FROM c WHERE ARRAY_CONTAINS(c.zipcodes, "{0}", true)'.format(message[2])
        zoneresult = CosmosFramework.QueryItems(cosmosdbquery=zonequery,container='zone')
        if zoneresult: #Meaning zipcode found
            if zoneresult[0]['id'] in zonelist:
                zonelist.remove(zoneresult[0]['id'])
                returnmessage += 'Weather Zone: {0} removed from server for County: **{1}** State: **{2}** \n'.format(zoneresult[0]['id'],zoneresult[0]['name'],zoneresult[0]['state'])
            else:
                returnmessage += 'Weather Area Code not listed in server, locations are stored at county level.'
        else:
            returnmessage = "Weather Zone not found for this zip code, try nearby zip code. Alerts are done at County level"
        serverresult['geocodes'] = zonelist
        CosmosFramework.ReplaceItem(serverresult['_self'],serverresult)
    except:
        returnmessage = "Error occurred while removing Zone to server"
    finally:
        return returnmessage

def severity(body:dict) -> str:
    serverresult = __get_server_info(body['guildid'])
    if serverresult['severity'] == 'moderate':
        serverresult['severity'] = 'severe'
        returnmessage = "Server severity level has been set to severe/extreme alerts only."
    elif serverresult['severity'] == 'severe':
        serverresult['severity'] = 'moderate'
        returnmessage = "Server severity level has been set to moderate/severe/extreme alerts only."
    CosmosFramework.ReplaceItem(serverresult['_self'],serverresult)
    return returnmessage

def help(body:dict) -> dict:
    returnembed = {}
    returnembed['title'] = 'Server Help'
    helpmessage = 'All commands must be issued by admin and mentioning the bot \n \
        Example: @Weather Alert Bot channel #general \n \
        Following Commands are available: \n \
        status - Returns Server Status \n \
        channel - Mention the channel you want alerts to be published in \n \
        severity - Changes severity level you get \n \
        help - Displays this help message \n \
        ping - Changes whether or not bot should @ everyone when publishing alerts (Note: Moderate alerts are never pinged regardless of server setting) \n \
        locationadd - put in location of zip code you want alerts for (See note about locations) \n \
        locationremove - put in location of zip code you no longer want alerts for (See note about locations) \n \
        Location Notes: National Weather Service Weather alerts operate at US County level and thus bot operates at county level as well. If you did location add 20001 \
        and 20002, both Washington DC zip codes, it will still only be one zone. Thus, most servers probably only need a few zip codes entered to cover geographical area'
    returnembed['description'] = helpmessage
    return returnembed

