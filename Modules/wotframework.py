import Modules.CommonFramework as CommonFramework
from typing import Tuple, List, Iterator, Any

def GetPlayersClanInfo(wgids : List[int]) -> List[Tuple[int, int, str]]:
    apikey = CommonFramework.RetrieveConfigOptions("wargaming")
    apikey = apikey['apitoken']
    wgids = ",".join(map(str, wgids))
    uri = "https://api.worldoftanks.com/wgn/clans/membersinfo/?application_id={0}&account_id={1}".format(str(apikey), wgids)
    playerData = CommonFramework.get_json_data(uri) # type: dict

    def getInfo(rawinfo : Tuple[str, Any]) -> Tuple[int, int, str]:
        wgid, info = rawinfo
        clan = info['clan']['clan_id'] if info is not None else None
        role = info['role'] if info is not None else None
        return int(wgid), clan, role

    return list(map(getInfo, playerData['data'].items()))

def GetClanInfo(wgclanid:int) -> dict:
    apikey = CommonFramework.RetrieveConfigOptions("wargaming")
    apikey = apikey['apitoken']
    uri = ""

def player_data_info(wgid:List[int]) -> dict:
    apikey = CommonFramework.RetrieveConfigOptions("wargaming")
    apikey = apikey['apitoken']
    if len(wgid) > 100:
        return None
    else:
        wgidcsv = ""
        for wid in wgid:
            wgidcsv += "{0},".format(wid)
        wgidcsv = wgidcsv[:-1]
        uri = 'https://api.worldoftanks.com/wot/account/info/?application_id={0}&account_id={1}&extra=statistics.random'.format(apikey,wgidcsv)
        playerdata = CommonFramework.get_json_data(uri)
        return playerdata

def get_gm_elo_data(top:int) -> dict:
    """Gets top clans by ELO for Global Map"""
    wgapi = CommonFramework.RetrieveConfigOptions('wargaming')
    uri = "https://api.worldoftanks.com/wot/clanratings/top/ \
    ?application_id={0}&rank_field=gm_elo_rating&limit={1}".format(wgapi['apitoken'],top)
    apiresults = CommonFramework.get_json_data(uri)
    return apiresults