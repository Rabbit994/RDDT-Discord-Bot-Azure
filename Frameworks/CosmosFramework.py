import json as json
import azure.cosmos.cosmos_client as cosmos_client
import Frameworks.CommonFramework as CommonFramework


def SetupCosmosDB():
        config = CommonFramework.RetrieveConfigOptions("cosmosdb")
        cosmosclient = cosmos_client.CosmosClient(url_connection=config['ENDPOINT'],auth={'masterKey': config['PRIMARYKEY']})
        db = next((data for data in cosmosclient.ReadDatabases() if data['id'] == config['DATABASE']))
        coll = next((coll for coll in cosmosclient.ReadContainers(db['_self']) if coll['id'] == config['CONTAINER']))
        return cosmosclient, coll

def Query(cosmosdbquery):
        '''Queries CosmosDB and returns results.'''
        cosmosclient, coll = SetupCosmosDB()
        query = {'query': str(cosmosdbquery)}
        options = {"enableCrossPartitionQuery": True}
        resultreturn = cosmosclient.QueryItems(coll['_self'],query,options)
        results = list(resultreturn)
        return results

def InsertItem(cosmosdbquery):
        '''Inserts Item into CosmosDB, Expects Dict'''
        cosmosclient, coll = SetupCosmosDB()
        resultreturn = cosmosclient.CreateItem(coll['_self'], cosmosdbquery, options=None)
        return resultreturn
        


        