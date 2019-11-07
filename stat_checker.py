#local modules
import Modules.CosmosFramework as CosmosFramework
import Modules.DiscordBotFramework as DiscordBotFramework
import Modules.DiscordFramework as DiscordFramework
import Modules.wotframework as wotframework

def UpdateStats() -> None:
    stattocheck = 'explosion_hits_received' #TODO
    results = CosmosFramework.QueryItems('SELECT c.wgid FROM c WHERE c.wgid <> null','users')
    wgidlist = []
    for result in results:
        if len(wgidlist) < 99:
            wgidlist.append(result['wgid'])
        else:
            wgidlist.append(result['wgid'])
            wgapiresults = wotframework.player_data_info(wgidlist)
            wgapiresults = wgapiresults['data']
            for wgapiresult in wgapiresults.items():
                wgapiresult = wgapiresult[1]
                if wgapiresult is None:
                    continue
                userdbdata = CosmosFramework.query_cosmos_for_user_by_wgid(wgapiresult['account_id'])
                if userdbdata is None:
                    continue
                if 'contest' in userdbdata: #Meaning I've seen user before
                    stat = wgapiresult['statistics']['random'][stattocheck]
                    userdbdata['contest']['points'].append(stat)
                    if (int(stat) - int(userdbdata['contest']['points'][0]) != 0):
                        userdbdata['contest']['currentscore'] = int(stat) - int(userdbdata['contest']['points'][0])
                    #CosmosFramework.ReplaceItem(userdbdata['_self'],userdbdata) ##TODO Verify that this works
                elif 'contest' not in userdbdata:
                    stat = [wgapiresult['statistics']['random'][stattocheck]]
                    points = {'points':stat}
                    points['currentscore'] = 0
                    userdbdata['contest'] = dict(points)
                    CosmosFramework.ReplaceItem(userdbdata['_self'],userdbdata)
            wgidlist.clear()


while True:
    try:
        UpdateStats()
        time.sleep(3600*4)
    except:
        raise Exception

        
    

