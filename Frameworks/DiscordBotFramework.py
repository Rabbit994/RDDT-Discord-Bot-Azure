import Frameworks.CosmosFramework as CosmosFramework
import Frameworks.DiscordFramework as DiscordFramework

#Public def
async def register(message: object) -> dict:
    """Registration Information"""
    returnmessage = dict()
    result = CosmosFramework.QueryItems('SELECT * FROM c WHERE c.discordid = "{0}"'.format(message.author.id))
    result = result[0]
    if result['wgid'] is not None:
        returnmessage['private'] = "You have already registered"
    elif result['token'] is not None:
        returnmessage['private'] = ""


#Private def