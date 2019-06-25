import json
import os

def RetrieveConfigOptions(key):
    try:
        jsonpath = os.path.abspath('.\\parameters\\parameters.json')
        with open(jsonpath,'r') as json_file:
            data = json.load(json_file)
        return data[key]
    except:
        raise Exception(f'Failure on Config load')
