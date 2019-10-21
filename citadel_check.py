import json
##Local Modules
import Modules.CommonFramework as CommonFramework
import Modules.CosmosFramework as CosmosFramework
import Modules.wotframework as wotframework

##TODO Get criteria 
#Criteria are rank and member of CW clan
#

def run_citadel_check():
    def __get_citadel_results() -> dict:
        primary = {}
        secondary = {}
        results = CosmosFramework.QueryItems('SELECT * FROM c','citadel')
        for result in results:
            secondary['tag'] = result['tag']
            secondary['name'] = result['name']
            secondary['citadel'] = result['citadel']
            secondary['override'] = result['citadeloverride']
            secondary['excludereason'] = result['excludereason']
            secondary['excludetime'] = result['excludetime']
            primary[result['wgid']] = secondary
            secondary.clear()

    wgapi = CommonFramework.RetrieveConfigOptions('wargaming')
    results = __get_citadel_results()
    apiresults = CommonFramework.get_json_data("https://api.worldoftanks.com/wot/clanratings/top/?application_id={0}&rank_field=gm_elo_rating&limit=200".format(wgapi['apitoken']))
    for apiresult in apiresults['data']:
        wgidlist = []
        wgidlist.append(apiresult['clan_id'])
        if apiresult['clan_id'] not in results:
            item = {}
            item['wgid'] = apiresult['clan_id']
            item['name'] = apiresult['clan_name']
            item['tag'] = apiresult['clan_tag']
            item['citadel'] = True
            CosmosFramework.InsertItem(item,'citadel')
        elif apiresult['clan_id'] in results and (results[apiresult['clan_id']]['tag'] != apiresult['clantag'] or results[apiresult['clan_id']]['name'] != apiresult['clan_name']):
            updateitem = CosmosFramework.QueryItems('SELECT * FROM c WHERE c.wgid={0}'.format(apiresult['clan_id']),'citadel')
            updateitem = updateitem[0]
            updateitem['name'] = apiresult['clan_name']
            updateitem['tag'] = apiresult['clan_tag']
            CosmosFramework

        pass


run_citadel_check()
