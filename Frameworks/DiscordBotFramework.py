import Frameworks.CosmosFramework as CosmosFramework
import Frameworks.DiscordFramework as DiscordFramework
import hashlib
import datetime

#Public def
async def register(message: object) -> dict:
    """Registration"""
    def genToken(discordId):
        time = str(datetime.datetime.utcnow().microsecond) # only microseconds in last second. i.e. <100
        hasher = hashlib.sha256(discordId.encode('utf-8'))
        hasher.update(time.encode('utf-8'))
        return hasher.hexdigest()[-8:]
    
    authordiscordid = message.author.id
    returnmessage = dict()
    result = CosmosFramework.QueryItems('SELECT * FROM c WHERE c.discordid = "{0}"'.format(authordiscordid))
    result = result[0]
    if bool(result):
        document = dict()
        document['discordid'] = authordiscordid
        document['wgtoken'] = str(genToken(authordiscordid))
    elif result['wgid'] is not None:
        returnmessage['private'] = "You have already registered"
    elif result['token'] is not None:
        returnmessage['private'] = ""


#Private def