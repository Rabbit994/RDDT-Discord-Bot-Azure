import json
import os
import urllib.request
import ssl

def RetrieveConfigOptions(key:str) -> dict:
    try:
        jsonpath = os.path.abspath('./parameters/parameters.json')
        with open(jsonpath,'r') as json_file:
            data = json.load(json_file)
        return data[key]
    except:
        raise Exception(f'Failure on Config load')

def get_json_data(uri: str) -> dict:
    """Returns JSON Data in dict format"""
    try:
        response = urllib.request.urlopen(uri,timeout=60)
        urldata = response.read().decode("utf-8","ignore")
        jsondata = json.loads(urldata)
        return jsondata
    except:
        return None

def convert_date_time_epoch(datetime:str) -> int:
    """Convert Datetime into epoch"""
    import dateutil.parser as dp
    parsed_t = dp.parse(datetime)
    t_in_seconds = parsed_t.timestamp()
    return int(t_in_seconds)

def GetClanBattles(clanid:int):
    def clantools_get_json_data(uri: str) -> dict:
        #This is fix for clantools certificate always expiring
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            response = urllib.request.urlopen(uri, timeout=60, context=ctx)
            urldata = response.read().decode("utf-8","ignore")
            jsondata = json.loads(urldata)
            return jsondata
        except:
            return None
    
    clantoolsurl = 'https://sv.clantools.us/integrations/battles/report?provider=na&tz=et&service=slack&clan_id={0}'.format(clanid)
    data = clantools_get_json_data(clantoolsurl)
    return data