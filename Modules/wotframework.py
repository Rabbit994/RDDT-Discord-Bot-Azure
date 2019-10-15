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

