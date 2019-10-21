import json
import time
##Local Modules
import Modules.CommonFramework as CommonFramework
import Modules.CosmosFramework as CosmosFramework
import Modules.wotframework as wotframework
import Modules.DiscordFramework as DiscordFramework

def run_citadel_check():
    def __get_citadel_results() -> dict:
        primary = {}
        secondary = {}
        results = CosmosFramework.QueryItems('SELECT * FROM c','citadel')
        for result in results:
            secondary['tag'] = result.get('tag')
            secondary['name'] = result.get('name')
            secondary['citadel'] = result.get('citadel')
            secondary['override'] = result.get('citadeloverride') 
            secondary['excludereason'] = result.get('excludereason') 
            secondary['excludetime'] = result.get('excludetime')
            primary[result['wgid']] = dict(secondary)
            secondary.clear()
        return primary

    citadelchannelid = 491800495980150789
    wgapi = CommonFramework.RetrieveConfigOptions('wargaming')
    results = __get_citadel_results()
    apiresults = CommonFramework.get_json_data("https://api.worldoftanks.com/wot/clanratings/top/?application_id={0}&rank_field=gm_elo_rating&limit=200".format(wgapi['apitoken']))
    wgidlist = []
    for apiresult in apiresults['data']:
        wgidlist.append(apiresult['clan_id'])
        if apiresult['clan_id'] not in results:
            item = {}
            item['wgid'] = apiresult['clan_id']
            item['name'] = apiresult['clan_name']
            item['tag'] = apiresult['clan_tag']
            item['citadel'] = True
            CosmosFramework.InsertItem(item,'citadel')
        elif apiresult['clan_id'] in results and (results[apiresult['clan_id']]['tag'] != apiresult['clan_tag'] or results[apiresult['clan_id']]['name'] != apiresult['clan_name']):
            updateitem = CosmosFramework.QueryItems('SELECT * FROM c WHERE c.wgid={0}'.format(apiresult['clan_id']),'citadel')
            updateitem = updateitem[0]
            updateitem['name'] = apiresult['clan_name']
            updateitem['tag'] = apiresult['clan_tag']
            CosmosFramework.ReplaceItem(updateitem['_self'],updateitem)
    clanlist = list(results.keys())
    removeclans = list(set(clanlist) - set(wgidlist)) #List of clans that are removed
    for removeclan in removeclans:
        claninfo = CosmosFramework.QueryItems('SELECT * FROM c WHERE c.wgid={0}'.format(removeclan),'citadel')
        claninfo = claninfo[0]
        if 'override' in claninfo and claninfo['override'] is True:
            continue #Overrides are not removed
        elif 'excludetime' not in claninfo:
            claninfo['excludetime'] = int(time.time()) + 604800
            message = "WARNING: Clan {0} ({1}) will be removed within 7 days due to lack of ELO rating.".format(claninfo['name'],claninfo['tag'])
            DiscordFramework.SendDiscordMessage(message,citadelchannelid)
            CosmosFramework.ReplaceItem(claninfo['_self'],claninfo)
        elif claninfo['excludetime'] < int(time.time()):
            claninfo['citadel'] = False
            claninfo['excludereason'] = "Excluded by falling off ELO"


try:
    run_citadel_check()
    print("Run Complete")
    time.sleep((60*60) * 6)
except:
    #raise Exception
    time.sleep((60*60) * 6)