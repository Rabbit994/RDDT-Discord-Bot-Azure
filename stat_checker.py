import time
import random
#local modules
import Modules.CommonFramework as CommonFramework
import Modules.CosmosFramework as CosmosFramework
import Modules.DiscordBotFramework as DiscordBotFramework
import Modules.DiscordFramework as DiscordFramework
import Modules.wotframework as wotframework

def UpdateStats() -> None:
    channelid = 491800495980150789

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
    
    def __post_contest_results(channelid:str,statrandom:bool=True) -> None:
        """Posts Contest results, Needs Channel ID and if results should be randomized"""
        results = CosmosFramework.QueryItems('SELECT TOP 3 * FROM c WHERE IS_DEFINED(c.contest.currentscore) AND c.contest.currentscore != 0 ORDER BY c.contest.currentscore DESC','users')
        if not bool(results): ##No users with score greater then 1
            return None
        config = CommonFramework.RetrieveConfigOptions('discord')
        place = 1
        DiscordFramework.SendDiscordMessage('Current Contest results:', channelid)
        for result in results:
            userdata = DiscordFramework.get_user_guild_info(result['discordid'],config['serverid'])
            if result['contest']['currentscore'] == 0:
                place += 1
                continue
            if 'code' in userdata and userdata['code'] == 10007:
                CosmosFramework.delete_user_from_cosmos_by_discordid(result['discordid'])
                continue
            if userdata['nick'] is None:
                nick = userdata['user']['username']
            else:
                nick = userdata['nick']
            if statrandom is True:
                score = int(result['contest']['currentscore'] * (random.randint(100,110)/100))
            else:
                score = int(result['contest']['currentscore'])
            discordmessage = "{0} is currently in #{1} place with score: {2}".format(nick,place,score)
            DiscordFramework.SendDiscordMessage(discordmessage,channelid)
            place += 1

    def __end_current_contest(channelid:str) -> None:
        contestresults = CosmosFramework.QueryItems('SELECT * FROM c WHERE c.active = true','contest')
        winnerresults = CosmosFramework.QueryItems('SELECT TOP 3 * FROM c WHERE IS_DEFINED(c.contest.currentscore) AND c.contest.currentscore != 0 ORDER BY c.contest.currentscore DESC','users')
        contestresults = contestresults[0]
        message = 'Contest is over, congratulations to the winners. Stat being tracked this contest was: {0}. Rewards will be issued shortly.'.format(contestresults['stat'])
        DiscordFramework.SendDiscordMessage(message=message,channelid=channelid)
        placedict = {}
        place = 1
        for result in winnerresults:
            placedict[str(place)] = {result['wgid']: result['contest']['currentscore']}
            place += 1
        contestresults['winners'] = dict(placedict)
        contestresults['active'] = False
        CosmosFramework.ReplaceItem(contestresults['_self'],contestresults)

    
    currenttime = int(time.time())
    contestresults = CosmosFramework.QueryItems('SELECT * FROM c WHERE c.active = true OR c.start = true','contest')
    if not bool(contestresults):
        return None #No contest is currently running, abort
    contestresults = contestresults[0]
    stattocheck = contestresults['stat']
    #Start New Contest
    if contestresults['start'] == True:
        __start_new_contest(channelid)
    
    #Update all WGID
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

    #Post Contest Results
    
    if contestresults['endtime'] < currenttime:
        __post_contest_results(channelid=channelid,statrandom=False)
        __end_current_contest(channelid=channelid)
    else:
        __post_contest_results(channelid=channelid,statrandom=True)


while True:
    try:
        UpdateStats()
        print("Update finished")
        time.sleep(3600*4)
    except:
        raise Exception

        
    

