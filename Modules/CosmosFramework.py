import json as json
import azure.cosmos.cosmos_client as cosmos_client
import os
import Modules.CommonFramework as CommonFramework

def SetupCosmosDB(container=None):
        #Azure Function Setup
        config = CommonFramework.RetrieveConfigOptions("cosmosdb")
        cosmosclient = cosmos_client.CosmosClient(url_connection=config['ENDPOINT'],auth={'masterKey': config['PRIMARYKEY']})
        db = next((data for data in cosmosclient.ReadDatabases() if data['id'] == config['DATABASE']))
        if container is None:
                coll = next((coll for coll in cosmosclient.ReadContainers(db['_self']) if coll['id'] == config['CONTAINER']))
        else:
                coll = next((coll for coll in cosmosclient.ReadContainers(db['_self']) if coll['id'] == str(container)))
        return cosmosclient, coll

def QueryItems(cosmosdbquery:str, container:str=None) -> list:
        '''Queries CosmosDB and returns results.'''
        cosmosclient, coll = SetupCosmosDB(container)
        query = {'query': str(cosmosdbquery)}
        options = {"enableCrossPartitionQuery": True}
        resultreturn = cosmosclient.QueryItems(coll['_self'],query,options)
        results = list(resultreturn)
        return results

def InsertItem(document:dict, container:str=None) -> dict:
        '''Inserts Item into CosmosDB, Expects Dict, returns document inserted'''
        cosmosclient, coll = SetupCosmosDB(container)
        try:
                resultreturn = cosmosclient.CreateItem(coll['_self'], document, options=None)
                return resultreturn
        except:
                raise Exception

def RemoveItem(documentid,partitionid):
        '''Deletes item from CosmosDB, expects _self (Document Link) and Cosmos DB partition Key (for this application, that's Discord ID)'''
        cosmosclient, coll = SetupCosmosDB()
        options = {"enableCrossPartitionQuery": True}
        options['partitionKey'] = partitionid
        try:
                cosmosclient.DeleteItem(str(documentid),options)
        except:
                raise Exception
        return

def ReplaceItem(documentlink:str,newdocument:dict) -> list:
        '''Replaces existing item with new item'''
        cosmosclient, coll = SetupCosmosDB()
        try:
                resultreturn = cosmosclient.ReplaceItem(documentlink,newdocument)
        except:
                raise Exception
        return resultreturn

def query_cosmos_for_user_by_wgid(wgid:int) -> None:
        '''Gets user CosmosDB entry by wgid'''
        results = QueryItems('SELECT * FROM c WHERE c.wgid = {0}'.format(wgid),'users')
        if not bool(results):
                return None
        else:
                return results[0]

def delete_user_from_cosmos_by_discordid(discordid:str) -> None:
        '''Deletes user from database by Discord ID'''
        results = QueryItems('SELECT * FROM c WHERE c.discordid = "{0}"'.format(discordid),'users')
        results = results[0]
        RemoveItem(results['_self'],results['discordid'])