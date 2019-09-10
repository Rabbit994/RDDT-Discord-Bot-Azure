import json
import asyncio
import Modules.CosmosFramework as CosmosFramework
import Modules.CommonFramework as CommonFramework

def get_checkpoint(eventhub:str) -> int:
    """Gets Event Position from CosmosDB"""
    config = CommonFramework.RetrieveConfigOptions('checkpoint')
    results = CosmosFramework.QueryItems('SELECT * FROM c WHERE c.eventhub = "{0}"'.format(eventhub),config['container'])
    results = results[0]
    return int(results['eventposition'])

async def set_checkpoint(eventhub:str,position:int) -> None: #async as this can be set in background
    """Sets Event Position in CosmosDB"""
    results = CosmosFramework.QueryItems('SELECT * FROM c WHERE c.eventhub = "{0}"'.format(eventhub))
    results[0]['eventposition'] = int(position)
    CosmosFramework.ReplaceItem(results[0]['_self'],results[0])
    return None
