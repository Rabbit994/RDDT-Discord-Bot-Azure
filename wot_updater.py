#This module handles World of Tanks Clan Updates
from time import sleep

import Modules.CosmosFramework as CosmosFramework
import Modules.wotframework as wotframework
import Modules.DiscordBotFramework as DiscordBotFramework

def RunUpdate():
    
    def get_responsible_clans():
        results = CosmosFramework.QueryItems("SELECT DISTINCT(c.wotclan) FROM c WHERE c.wotclan <> null",'roles')
        returnlist = []
        for result in results:
            returnlist.append(result['wotclan'])
        return returnlist

    familyclans = get_responsible_clans()

    results = CosmosFramework.QueryItems("SELECT * FROM c WHERE c.wgid <> null AND c.server = 'NA'")
    users = {}
    userinfo = {}
    for result in results:
        userinfo.clear()
        userinfo['clan'] = result['clan']
        userinfo['rank'] = result['rank']
        #userinfo['wgid'] = result['wgid']
        userinfo['discordid'] = result['discordid']
        users[result['wgid']] = dict(userinfo)
    listofusers = []
    wotresults = []
    for user in users:
        if len(listofusers) < 100:
            listofusers.append(user)
        else:
            wotresults += wotframework.GetPlayersClanInfo(listofusers)
            listofusers.clear()
    wotresults += wotframework.GetPlayersClanInfo(listofusers)
    for wotresult in wotresults:
        if wotresult[1] in familyclans: #check if they are in family
            if users[wotresult[0]]['clan'] != wotresult[1] or users[wotresult[0]]['rank'] != wotresult[2]:
                results = CosmosFramework.QueryItems("SELECT * FROM c WHERE c.wgid={0}".format(wotresult[0]),'users')
                results = results[0]
                results['clan'] = wotresult[1]
                results['rank'] = wotresult[2]
                CosmosFramework.ReplaceItem(results['_self'],results)
                #TODO Send Update
                DiscordBotFramework.checkroles(results['discordid'])
        else:
            if users[wotresult[0]]['clan'] != wotresult[1] or users[wotresult[0]]['rank'] != 'friend':
                results = CosmosFramework.QueryItems("SELECT * FROM c WHERE c.wgid={0}".format(wotresult[0]),'users')
                results = results[0]
                results['clan'] = wotresult[1]
                results['rank'] = 'friend'
                CosmosFramework.ReplaceItem(results['_self'],results)
                #TODO Send Update
                DiscordBotFramework.checkroles(results['discordid'])
                

RunUpdate()
sleep(900) #Sleep for 15 minutes before restarting