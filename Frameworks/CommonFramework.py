import json
import os
def RetrieveConfigOptions(key):
    #Next two lines are because python hates dealing with paths on Windows
    #cur_path = os.path.dirname(__file__)
    #new_path = os.path.relpath('\\parameters\\parameters.json', cur_path)
    try:
        jsonpath = os.path.abspath('.\\parameters\\parameters.json')
        with open(jsonpath,'r') as json_file:
            data = json.load(json_file)
        return data[key]
    except:
        raise Exception(f'Failure on Config load')
