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
        results = CosmosFramework.QueryItems('SELECT * FROM c WHERE c.citadel = true','citadel')
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

    def __exclude_clan_from_citadel(clanid):
        citadelroleid = 636372439261249566
        discordserverid = CommonFramework.RetrieveConfigOptions('discord')
        discordserverid = discordserverid['serverid']
        results = CosmosFramework.QueryItems('SELECT * FROM c WHERE c.clan = {0} AND c.citadel = true'.format(clanid))
        for result in results:
            status_code = DiscordFramework.RemoveUserRole(citadelroleid,result['discordid'],discordserverid)
            if status_code == 204:
                del result['citadel']
                CosmosFramework.ReplaceItem(result['_self'],result)
            else:
                DiscordFramework.send_discord_private_message("Citadel checker is having issues",113304266269003776)
                raise "Clan removal failed"
    
    def __exclude_wgid_from_citadel(wgid:int) -> None:
        """Removes WGID from citadel"""
        citadelroleid = 636372439261249566
        discordserverid = CommonFramework.RetrieveConfigOptions('discord')
        discordserverid = discordserverid['serverid']
        result = CosmosFramework.QueryItems('SELECT * FROM c WHERE c.discordid="{0}"'.format(wgid),'users')
        if bool(result):
            result = result[0]
            DiscordFramework.RemoveUserRole(citadelroleid,result['discordid'],discordserverid)
            DiscordFramework.send_discord_private_message('You have been removed from RDDT citadel due clan/rank changes',result['discordid'])
            del result['citadel']
            CosmosFramework.ReplaceItem(result['_self'],result)
      
    citadelchannelid = 636374196355858452 #Actual citadel channel
    wgapi = CommonFramework.RetrieveConfigOptions('wargaming')
    results = __get_citadel_results()
    apiresults = CommonFramework.get_json_data("https://api.worldoftanks.com/wot/clanratings/top/?application_id={0}&rank_field=gm_elo_rating&limit=200".format(wgapi['apitoken']))
    wgidlist = []
    #Do clan checks ##TODO put this in it's own def block
    for apiresult in apiresults['data']: #Get information about clans from Wargaming API
        wgidlist.append(apiresult['clan_id'])
        if apiresult['clan_id'] not in results:
            item = {}
            item['wgid'] = apiresult['clan_id']
            item['name'] = apiresult['clan_name']
            item['tag'] = apiresult['clan_tag']
            item['citadel'] = True
            CosmosFramework.InsertItem(item,'citadel')
        elif apiresult['clan_id'] in results and (results[apiresult['clan_id']]['tag'] != apiresult['clan_tag'] or results[apiresult['clan_id']]['name'] != apiresult['clan_name']):
            #Checks the database and Wargaming API match around clan tag and name, if not, it updates it
            updateitem = CosmosFramework.QueryItems('SELECT * FROM c WHERE c.wgid={0}'.format(apiresult['clan_id']),'citadel')
            updateitem = updateitem[0]
            updateitem['name'] = apiresult['clan_name']
            updateitem['tag'] = apiresult['clan_tag']
            CosmosFramework.ReplaceItem(updateitem['_self'],updateitem)
    clanlist = list(results.keys())
    removeclans = list(set(clanlist) - set(wgidlist)) #List of clans to be removed
    for removeclan in removeclans:
        claninfo = CosmosFramework.QueryItems('SELECT * FROM c WHERE c.wgid={0}'.format(removeclan),'citadel')
        claninfo = claninfo[0]
        if 'override' in claninfo and claninfo['override'] is True:
            continue #Overrides are not removed
        elif 'excludetime' not in claninfo: #Step 2, put in removal time
            claninfo['excludetime'] = int(time.time()) + 604700 #This is 6 days, 23 hours and ~58 minutes
            message = "WARNING: Clan {0} ({1}) will be removed within 7 days due to lack of clan rating.".format(claninfo['name'],claninfo['tag'])
            DiscordFramework.SendDiscordMessage(message,citadelchannelid)
            CosmosFramework.ReplaceItem(claninfo['_self'],claninfo)
        elif claninfo['excludetime'] < int(time.time()): #when their time is hit, mark them no longer allowed in citadel with reason and remove all clan members
            __exclude_clan_from_citadel(removeclan)
            message = "Clan {0} ({1}) has been removed from citadel.".format(claninfo['name'],claninfo['tag'])
            DiscordFramework.SendDiscordMessage(message,citadelchannelid)
            claninfo['citadel'] = False
            claninfo['excludetime'] = None
            claninfo['excludereason'] = 'Excluded due to lack of ranking'
            CosmosFramework.ReplaceItem(claninfo['_self'],claninfo)
    #Do user checks ##TODO Put this in it's own def block
    userresults = CosmosFramework.QueryItems('SELECT c.wgid FROM c WHERE c.citadel = true','users')
    wgidtocheck = []
    for userresult in userresults:
        wgidtocheck.append(userresult['wgid'])
        if len(wgidtocheck) >= 99:
            apiresults = wotframework.GetPlayersClanInfo(wgidtocheck)
            for apiresult in apiresults:
                if apiresult[1] is None or apiresult[2] not in ['commander','executive_officer','combat_officer','personnel_officer']:
                    __exclude_wgid_from_citadel(apiresult[0])
            wgidtocheck.clear()

while True:
    try:
        run_citadel_check()
        print("Run Complete")
        time.sleep((60*60) * 6)
    except:
        time.sleep((60*60) * 6)
        raise Exception