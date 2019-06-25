from typing import Tuple, List, Iterator, Any
import os
import urllib.request
import json

from ..SharedCode import CosmosFramework

def __GetJSONData(uri: str) -> dict:
    """Returns JSON Data in dict format"""
    response = urllib.request.urlopen(uri)
    urldata = response.read().decode("utf-8","ignore")
    jsondata = json.loads(urldata)
    return jsondata

def GetPlayersClanInfo(wgids: List[int], region: str = "NA") -> List[Tuple[int, int, str]]:
    apikey = os.environ.get('WGAPIKEY')
    wgids = ",".join(map(str, wgids))
    uri = "https://api.worldoftanks.com/wgn/clans/membersinfo/?application_id=%s&account_id=%s" % (str(apikey), wgids)
    playerData = __GetJSONData(uri) # type: dict

    def getInfo(rawinfo : Tuple[str, Any]) -> Tuple[int, int, str]:
        wgid, info = rawinfo
        clan = info['clan']['clan_id'] if info is not None else None
        role = info['role'] if info is not None else None
        return int(wgid), clan, role

    return list(map(getInfo, playerData['data'].items()))

def GetClansResponsible(region : str = "NA") -> list:
    results = CosmosFramework.QueryItems('SELECT DISTINCT c.wotclan FROM c WHERE c.role = 1 AND c.wotclan != null AND c.wotserver = "{0}"'.format(region))
    clanreturn = []
    for result in results:
        clanreturn.append(int(result['wotclan']))
    return clanreturn
