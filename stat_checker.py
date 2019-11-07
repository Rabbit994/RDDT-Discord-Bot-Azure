import time
#local modules
import Modules.CosmosFramework as CosmosFramework
import Modules.DiscordBotFramework as DiscordBotFramework
import Modules.DiscordFramework as DiscordFramework
import Modules.wotframework as wotframework

def UpdateStats() -> None:
    
    def __update_list_of_wgid(wgid:list) -> None:
        """Updates a list of WGID, maximum of 100"""
        wgapiresults = wotframework.player_data_info(wgid)
        wgapiresults = wgapiresults['data']
        for wgapiresult in wgapiresults.items():
            wgapiresult = wgapiresult[1]
            if wgapiresult is None:
                continue #Unknown user, skip
            userdbdata = CosmosFramework.query_cosmos_for_user_by_wgid(wgapiresult['account_id'])
            if userdbdata is None:
                continue #Not in database, This shouldn't happen
            if 'contest' in userdbdata: #Meaning I've seen user before
                stat = wgapiresult['statistics']['random'][stattocheck]
                userdbdata['contest']['points'].append(stat)
                if (int(stat) - int(userdbdata['contest']['points'][0]) != 0):
                    userdbdata['contest']['currentscore'] = int(stat) - int(userdbdata['contest']['points'][0])
                CosmosFramework.ReplaceItem(userdbdata['_self'],userdbdata)
            elif 'contest' not in userdbdata:
                stat = [wgapiresult['statistics']['random'][stattocheck]]
                points = {'points':stat}
                points['currentscore'] = 0
                userdbdata['contest'] = dict(points)
                CosmosFramework.ReplaceItem(userdbdata['_self'],userdbdata)

    def __start_new_contest() -> None:
        
        pass
    ##TODO handle starting contest
    currenttime = int(time.time())
    endtime = currenttime + (86400 * 14) #Number of days
    results = CosmosFramework.QueryItems('SELECT * FROM c WHERE c.starttime > {0} and c.endtime < {1}'.format(currenttime,endtime),'contest')
    if not bool(results):
        __start_new_contest()

    stattocheck = 'explosion_hits_received' #TODO Move to Config file or randomizer
    results = CosmosFramework.QueryItems('SELECT c.wgid FROM c WHERE c.wgid <> null','users')
    wgidlist = []
    for result in results:
        if len(wgidlist) < 99:
            wgidlist.append(result['wgid'])
        else:
            wgidlist.append(result['wgid'])
            __update_list_of_wgid(wgidlist)
            wgidlist.clear()
    __update_list_of_wgid(wgidlist)
    
    ##TODO Handle ending contest
    ##TODO Update Channel with information

while True:
    try:
        UpdateStats()
        time.sleep(3600*4)
    except:
        raise Exception

        
    

