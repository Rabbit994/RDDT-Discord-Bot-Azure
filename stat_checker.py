import time
import random
#local modules
import Modules.CommonFramework as CommonFramework
import Modules.CosmosFramework as CosmosFramework
import Modules.DiscordBotFramework as DiscordBotFramework
import Modules.DiscordFramework as DiscordFramework
import Modules.wotframework as wotframework

def UpdateStats() -> None:
    
    def __update_list_of_wgid(wgid:list, stattocheck:str) -> None:
        """Updates a list of WGID, maximum of 100"""
        wgapiresults = wotframework.player_data_info(wgid)
        wgapiresults = wgapiresults['data']
        for wgapiresult in wgapiresults.items():
            wgapiresult = wgapiresult[1]
            if wgapiresult is None:
                continue #Unknown user, skip (Banned, deleted user)
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

    def __start_new_contest(channelid:str) -> None:
        """Starts new contest by removing old contest results"""
        results = CosmosFramework.QueryItems('SELECT * FROM c WHERE IS_DEFINED(c.contest)')
        for result in results:
            del result['contest']
            CosmosFramework.ReplaceItem(result['_self'],result)
        results = CosmosFramework.QueryItems('SELECT * FROM c WHERE c.start = true','contest')
        results = results[0]
        results['start'] = False
        results['active'] = True
        CosmosFramework.ReplaceItem(results['_self'],results)
        days = int((results['endtime'] - results['starttime']) / 86400)
        DiscordFramework.SendDiscordMessage('A new contest has started! It will run for {0} days.'.format(days),channelid)
    
    channelid = 491800495980150789
    currenttime = int(time.time())
    contestresults = CosmosFramework.QueryItems('SELECT * FROM c WHERE c.active = true OR c.start = true','contest')
    if not bool(contestresults):
        return None #No contest is currently running, abort
    contestresults = contestresults[0]
    stattocheck = contestresults['stat']
    if contestresults['start'] == True:
        __start_new_contest(channelid)
    elif contestresults['endtime'] < currenttime:
        pass ##TODO End Contest
    
    results = CosmosFramework.QueryItems('SELECT c.wgid FROM c WHERE c.wgid <> null','users')
    wgidlist = []
    for result in results:
        if len(wgidlist) < 99:
            wgidlist.append(result['wgid'])
        else:
            wgidlist.append(result['wgid'])
            __update_list_of_wgid(wgidlist,stattocheck)
            time.sleep(3) #WG API rate limiting
            wgidlist.clear()
    __update_list_of_wgid(wgidlist,stattocheck)
    ##TODO Channel update
    results = CosmosFramework.QueryItems('SELECT TOP 3 * FROM c WHERE IS_DEFINED(c.contest.currentscore) AND c.contest.currentscore != 0 ORDER BY c.contest.currentscore DESC','contest')
    if not bool(results): ##No users with score greater then 1
        return None
    config = CommonFramework.RetrieveConfigOptions('discord')
    place = 1
    DiscordFramework.SendDiscordMessage('Current Contest results:',channelid)
    for result in results:
        userdata = DiscordFramework.get_user_guild_info(result['discordid'],config['serverid'])
        if result['contest']['currentscore'] == 0:
            place += 1
            continue
        if userdata['nick'] is None:
            nick = userdata['user']['username']
        else:
            nick = userdata['nick']
        score = userdata['contest']['currentscore'] * (random.randint(90,110)/100)
        discordmessage = "{0} is currently in #{1} place with score: {2}".format(nick,place,score)
        DiscordFramework.SendDiscordMessage(discordmessage,channelid)
        place += 1


while True:
    try:
        UpdateStats()
        time.sleep(3600*4)
    except:
        raise Exception

        
    

