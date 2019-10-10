import time
import Modules.CosmosFramework as CosmosFramework
import Modules.CommonFramework as CommonFramework
import Modules.DiscordFramework as DiscordFramework

def CheckCones() -> None:
    currenttime = int(time.time())
    results = CosmosFramework.QueryItems('SELECT * FROM c WHERE c.cone < {0}'.format(currenttime))
    if bool(results): #meaning people to process
        for result in results:
            status_code = __remove_cone_role(result['discordid'])
            if status_code == 204:
                del result['cone']
                CosmosFramework.ReplaceItem(result['_self'],result)

        
    

def __remove_cone_role(discordid:str) -> int:
    ConeOfShameDiscordId = '525870180505747467'
    config = CommonFramework.RetrieveConfigOptions('discord')
    status_code = DiscordFramework.RemoveUserRole(ConeOfShameDiscordId,discordid,config['serverid'])
    return status_code

try:
    CheckCones()
except:
    pass