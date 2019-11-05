import time
#local modules
import Modules.CosmosFramework as CosmosFramework
import Modules.DiscordBotFramework as DiscordBotFramework
import Modules.DiscordFramework as DiscordFramework
import Modules.wotframework as wotframework

def UpdateStats() -> None:
    updatetime = int(time.time())
    stattocheck = 'explosion_hits_received'
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
                userdbdata = CosmosFramework.QueryItems('SELECT * FROM c WHERE c.wgid = {0}'.format(wgapiresult['account_id']))
                userdbdata = userdbdata[0]
                if 'contest' in userdbdata: #Meaning I've seen user before
                    pass #TODO Add update
                elif 'contest' not in userdbdata:
                    stat = wgapiresult['statistics']['random'][stattocheck]
                    #TODO Figure out to handle stats
                print(wgapiresult)


while True:
    try:
        UpdateStats()
        time.sleep(3600*4)
    except:
        raise Exception

        
    

