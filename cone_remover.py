import time
from time import sleep
import Modules.CosmosFramework as CosmosFramework
import Modules.CommonFramework as CommonFramework
import Modules.DiscordFramework as DiscordFramework

def CheckCones() -> None:
    def __remove_cone_role(discordid:str) -> int:
        ConeOfShameDiscordId = '525870180505747467'
        config = CommonFramework.RetrieveConfigOptions('discord')
        status_code = DiscordFramework.RemoveUserRole(ConeOfShameDiscordId,discordid,config['serverid'])
        return status_code

    currenttime = int(time.time())
    results = CosmosFramework.QueryItems('SELECT * FROM c WHERE c.cone < {0}'.format(currenttime))
    if bool(results): #meaning people to process
        for result in results:
            status_code = __remove_cone_role(result['discordid'])
            if status_code == 204:
                del result['cone']
                CosmosFramework.ReplaceItem(result['_self'],result)

try:
    CheckCones()
    sleep(120) #Sleep for 2 minutes and then exit
except:
    sleep(120) #Sleep for 2 minutes and then exit
    pass