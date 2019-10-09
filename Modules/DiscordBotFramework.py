import hashlib
import datetime

import Modules.CommonFramework as CommonFramework
import Modules.CosmosFramework as CosmosFramework
import Modules.DiscordFramework as DiscordFramework

#Public def
async def register(message: object) -> dict:
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

    authordiscordid = message.author.id
    link = CommonFramework.RetrieveConfigOptions("registration")
    link = link['flaskuri']
    returnmessage = {}
    result = CosmosFramework.QueryItems('SELECT * FROM c WHERE c.discordid = "{0}"'.format(authordiscordid))
    if not bool(result): #meaning no result
        document = dict()
        document['discordid'] = str(authordiscordid) #Discord IDs are in strings
        document['wgtoken'] = str(genToken(str(authordiscordid)))
        CosmosFramework.InsertItem(document)
        returnmessage['channel'] = "Welcome {0}! Check your direct messages for a link.".format(message.author.display_name)
        returnmessage['author'] = genURL(document['wgtoken'])
    elif result[0]['wgid'] is not None:
        returnmessage['author'] = "You have already registered"
    elif result[0]['token'] is not None:
        returnmessage['author'] = genURL(document['wgtoken'])
    return returnmessage

async def info(message):
    returnmessage = dict()
    result = CosmosFramework.QueryItems('SELECT ')

def checkroles(discordid:str) -> None:
    def get_responsible_roles() -> list:
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

#Private def