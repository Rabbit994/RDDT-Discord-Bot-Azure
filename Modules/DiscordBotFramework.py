#This module handles the bot commands
#Outbound messages should be put back into dict and returned to message_handler for outbound message processing

import hashlib
import datetime
import time
import random

#Local Modules
import Modules.CommonFramework as CommonFramework
import Modules.CosmosFramework as CosmosFramework
import Modules.DiscordFramework as DiscordFramework
import Modules.wotframework as wotframework

#Public def
def register(message: dict) -> dict:
    """Registration"""
    def genToken(discordId: str) -> str:
        time = str(datetime.datetime.utcnow().microsecond) # only microseconds in last second. i.e. <100
        hasher = hashlib.sha256(discordId.encode('utf-8'))
        hasher.update(time.encode('utf-8'))
        return hasher.hexdigest()[-8:]
    
    def genURL(token: str) -> str:
        """Generate FLask URI"""
        link = CommonFramework.RetrieveConfigOptions("registration")
        link = link['flaskuri']
        return "{0}?token={1}".format(link,token)

    authordiscordid = message['authorid']
    link = CommonFramework.RetrieveConfigOptions("registration")
    link = link['flaskuri']
    returnmessage = {}
    result = CosmosFramework.QueryItems('SELECT * FROM c WHERE c.discordid = "{0}"'.format(authordiscordid))
    if not bool(result): #meaning no result
        document = {}
        document['discordid'] = str(authordiscordid) #Discord IDs are in strings
        document['wgtoken'] = str(genToken(str(authordiscordid)))
        CosmosFramework.InsertItem(document)
        returnmessage['channel'] = "Welcome {0}! Check your direct messages for a link.".format(message['authordisplayname'])
        returnmessage['author'] = genURL(document['wgtoken'])
    elif result[0]['wgid'] is not None:
        returnmessage['author'] = "You have already registered"
    elif result[0]['token'] is not None:
        returnmessage['author'] = genURL(document['wgtoken'])
    return returnmessage

def update(message):
    returnmessage = {}
    discordmessage = message['message'].split()
    try:
        discordid = int(discordmessage[1])
        results = CosmosFramework.QueryItems('SELECT * FROM c WHERE c.discordid="{0}"'.format(discordid),'users')
        if not bool(results): #unknown Discord id
            returnmessage['channel'] = "Unknown Discord ID"
            return returnmessage
        checkroles(str(discordid))
        returnmessage['channel'] = "Roles checked and adjusted. If roles do not match, it's likely Wargaming API or bot is not up to date. Wait 15 minutes and check again."
        return returnmessage
    except:
        returnmessage['channel'] = "You did not pass in numerical Discord ID. See Pizar/Canteen for how to get that information"
        return returnmessage

def status(message):
    discordmessage = message['message'].split()
    returnmessage = {}
    if len(discordmessage) < 2:
        returnmessage['author'] = "You did not supply Discord ID or User Mention"
    discordid = __discord_id_from_mention(discordmessage[1])
    try:
        discordid = int(discordid)
        result = __query_cosmos_for_info_by_discordid(str(discordid))
        if result is None:
            returnmessage['author'] = "User has not registered with the bot"
        elif result['wgtoken'] != '00000000':
            returnmessage['author'] = "User has requested registration but not completed registration"
        elif result['wgid'] is not None and result['rank'] is None:
            returnmessage['author'] = "User has registered properly but awaiting Wargaming API update"
        else:
            returnmessage['author'] = "User has completed registration"
        return returnmessage
    except:
        returnmessage['author'] = "An error has occurred"
        return returnmessage
             
def checkroles(discordid:str) -> None:
    """Checks user for proper roles"""
    def get_responsible_roles() -> list:
        """Gets a list of Discordid roles that bot thinks it's responsible for"""
        results = CosmosFramework.QueryItems("SELECT DISTINCT(c.discordid) FROM c",'roles')
        listofroles = []
        for result in results:
            listofroles.append(result['discordid'])
        return listofroles

    config = CommonFramework.RetrieveConfigOptions('discord')
    playerresult = CosmosFramework.QueryItems('SELECT * FROM c WHERE c.discordid="{0}"'.format(discordid),'users')
    if not bool(playerresult): #Meaning unknown Discord ID
        return None
    playerresult = playerresult[0]
    resproles = get_responsible_roles() #Roles controlled by the bot
    userroles = DiscordFramework.GetUserRoles(discordid,config['serverid'])
    if userroles == 0:
        return None #User unknown, exit
    if playerresult['rank'] == "friend":
        friendrole = CosmosFramework.QueryItems('SELECT * FROM c WHERE c.wotrank = "friend"','roles')
        friendrole = friendrole[0]
        friendrole = friendrole['discordid']
        if int(friendrole) not in userroles:
            DiscordFramework.AddUserRole(friendrole,discordid,config['serverid'])
        resproles.remove(friendrole)
    else:
        userrankrole = CosmosFramework.QueryItems('SELECT c.discordid FROM c WHERE c.wotrank ="{0}" AND c.wotclan = {1}'.format(playerresult['rank'],playerresult['clan']),'roles')
        userrankrole = userrankrole[0]['discordid']
        userclanrole = CosmosFramework.QueryItems('SELECT c.discordid FROM c WHERE c.wotclan = {0} AND c.wotrank = null'.format(playerresult['clan']),'roles')
        userclanrole = userclanrole[0]['discordid']
        if int(userrankrole) not in userroles or int(userclanrole) not in userroles:
            DiscordFramework.AddUserRole(userclanrole,discordid,config['serverid'])
            DiscordFramework.AddUserRole(userrankrole,discordid,config['serverid'])
        resproles.remove(userclanrole)
        resproles.remove(userrankrole)
    commonroles = set(int(i) for i in resproles) & set(userroles) #userroles comes back as int
    if bool(commonroles): #Meaning there is roles showing up that shouldn't be there
        for role in commonroles:
            DiscordFramework.RemoveUserRole(role,discordid,config['serverid'])
    return None

def cone(body:dict) -> dict:
    """Cones user, adds information to database and sends return messages"""
    discordmessage = body['message'].split()
    ConeOfShameDiscordId = '525870180505747467'
    returnmessage = {}
    config = CommonFramework.RetrieveConfigOptions('discord')
    try:
        if len(discordmessage) < 3:
            returnmessage['author'] = 'Invalid command format'
            return returnmessage
        timetocone = int(discordmessage[2])
        if timetocone > 2880:
            returnmessage['author'] = 'You cannot Cone someone longer then 2 days'
            return returnmessage
        discordid = int(__discord_id_from_mention(discordmessage[1])) ##Trys int to make sure it's int
        result = __query_cosmos_for_info_by_discordid(discordid)
        if result is None:
            newitem = {}
            newitem['discordid'] = str(discordid)
            result = CosmosFramework.InsertItem(newitem,'users')
        if 'cone' in result:
            returnmessage['author'] = 'User is already coned'
        statuscode = DiscordFramework.AddUserRole(ConeOfShameDiscordId,discordid,config['serverid'])
        if statuscode == 204: #Meaning add role was successful
            result['cone'] = int(time.time()) + (60 * int(timetocone))
            CosmosFramework.ReplaceItem(result['_self'],result)
            returnmessage['channel'] = '{0} muted user for {1} minutes'.format(body['authordisplayname'],timetocone)
            returnmessage['author'] = 'Cone issued as requested'
            returnmessage['targetdiscordid'] = discordid
            returnmessage['target'] = 'You were muted for {0} minutes by {1}'.format(timetocone,body['authordisplayname'])
    except Exception as e:
        returnmessage['author'] = 'Following error has occured: {0}'.format(e)
        
def citadel(body:dict) -> dict:
    returnmessage = {}
    citadelroleid = 636372439261249566
    citadelchannelid = 636374196355858452
    result = __query_cosmos_for_info_by_discordid(str(body['authorid']))
    discordserverid = CommonFramework.RetrieveConfigOptions('discord')
    discordserverid = discordserverid['serverid']
    if result is None or 'wgid' not in result:
        returnmessage['author'] = "You have not registered with the bot, this is mandatory. Please visit <#507725600073449482> to register or please complete registration."
        return returnmessage
    wgid = [int(result['wgid'])]
    claninfo = wotframework.GetPlayersClanInfo(wgid)
    claninfo = claninfo[0]
    if claninfo[1] is None:
        returnmessage['author'] = "You are not a member of clan, citadel access is denied" 
        return returnmessage
    elif claninfo[2] not in ['commander','executive_officer','combat_officer','personnel_officer']:
        returnmessage['author'] = "Citadel access is restricted to Clan officers only"
        return returnmessage
    results = CosmosFramework.QueryItems('SELECT * FROM c WHERE c.wgid = {0}'.format(claninfo[1]),'citadel')
    if bool(results): #Meaning their clan ID is in citadel container
        result = results[0]
        if result['citadel'] is True:
            DiscordFramework.AddUserRole(citadelroleid,body['authorid'],discordserverid)
            returnmessage['author'] = "Access granted"
            DiscordFramework.SendDiscordMessage("{0} from {1} has joined the citadel.".format(body['authordisplayname'],result['name']),citadelchannelid)
            result = __query_cosmos_for_info_by_discordid(str(body['authorid']))
            result['citadel'] = True
            CosmosFramework.ReplaceItem(result['_self'],result)
        else:
            returnmessage['author'] = 'Citadel access has been revoked because: {0}. If you believe access should be granted, please see moderator.'.format(result['excludereason'])
    else:
        returnmessage['author'] = 'Citadel access is restricted to clans who rank on Global Map ELO. If you believe access should be granted, please see moderator.'
    return returnmessage

def startcontest(body:dict) -> dict:
    """Starts the contest in database for contest"""
    returnmessage = {}
    currenttime = int(time.time())
    if str(body['authorid']) not in ['298272014005829642','113304266269003776']:
        returnmessage['author'] = 'You are not authorized to start a contest'
        return returnmessage
    discordmessage = __get_split_message(body['message'])
    try: #Catching user not sending number
        if int(discordmessage[1]) > 28:
            returnmessage['author'] = 'Contests may not be longer then 28 days'
            return returnmessage
        endtime = currenttime + (86400 * int(discordmessage[1]))
    except:
        returnmessage['author'] = 'You do not specify how long contests can be for'
        return returnmessage
    results = CosmosFramework.QueryItems('SELECT * FROM c WHERE c.active = true OR c.start = true','contest')
    if len(results) > 1:
        returnmessage['author'] = 'It appears multiple contests are currently underway at this time, please let rabbit know'
        return returnmessage
    elif len(results) == 1:
        returnmessage['author'] = 'Contest is currently under way'
        return returnmessage
    else:
        doc = {'starttime':int(currenttime)}
        doc['endtime'] = int(endtime)
        doc['active'] = False
        doc['start'] = True
        statlist = ['capture_points',
        'damage_dealt',
        'damage_received',
        'direct_hits_received',
        'dropped_capture_points',
        'explosion_hits',
        'explosion_hits_received',
        'frags',
        'hits',
        'piercings',
        'piercings_received',
        'shots',
        'spotted',
        'stun_assisted_damage',
        'stun_number',
        'survived_battles']
        doc['stat'] = statlist[(random.randint(0,len(statlist) - 1))]
        CosmosFramework.InsertItem(doc,'contest')
        returnmessage['author'] = 'Contest started for {0} days'.format(discordmessage[1])
        return returnmessage

#Private def

def __discord_id_from_mention(discordid:str) -> str:
    """Checks Discord ID from possible mention and returns Discord ID"""
    if discordid.startswith("<@!"): #This checks to see if Discord ID is actually a mention, if it is, unwrap the id
        discordid = discordid[3:-1] # format is <@!0123456789> and we need 0123456789
    elif discordid.startswith("<@"):
        discordid = discordid[2:-1] #If user hasn't change their nickname, mention becomes <@ instead of <@!
    return discordid

def __query_cosmos_for_info_by_discordid(discordid:str) -> dict:
    """Querys Cosmos for user info and returns first entry"""
    results = CosmosFramework.QueryItems('SELECT * FROM c WHERE c.discordid="{0}"'.format(discordid),'users')
    if not bool(results):
        return None
    else:
        return results[0]

def __get_split_message(message:str) -> list:
    discordmessage = message.split()
    return discordmessage