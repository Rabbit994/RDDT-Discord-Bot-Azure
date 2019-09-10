import json
import os
import urllib

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
    response = urllib.request.urlopen(uri)
    urldata = response.read().decode("utf-8","ignore")
    jsondata = json.loads(urldata)
    return jsondata

def convert_date_time_epoch(datetime:str) -> int:
    """Convert Datetime into epoch"""
    import dateutil.parser as dp
    parsed_t = dp.parse(datetime)
    t_in_seconds = parsed_t.timestamp()
    return int(t_in_seconds)