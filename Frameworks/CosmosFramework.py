import json as json
import azure.cosmos.cosmos_client as cosmos_client
import Frameworks.CommonFramework as CommonFramework


def SetupCosmosDB(container=None):
        config = CommonFramework.RetrieveConfigOptions("cosmosdb")
        cosmosclient = cosmos_client.CosmosClient(url_connection=config['ENDPOINT'],auth={'masterKey': config['PRIMARYKEY']})
        db = next((data for data in cosmosclient.ReadDatabases() if data['id'] == config['DATABASE']))
        if container is None:
                coll = next((coll for coll in cosmosclient.ReadContainers(db['_self']) if coll['id'] == config['CONTAINER']))
        else:
                coll = next((coll for coll in cosmosclient.ReadContainers(db['_self']) if coll['id'] == str(container)))
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
        '''Inserts Item into CosmosDB, Expects Dict, returns document inserted'''
        cosmosclient, coll = SetupCosmosDB()
        resultreturn = cosmosclient.CreateItem(coll['_self'], cosmosdbquery, options=None)
        return resultreturn

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

def ReplaceItem(documentlink,newdocument):
        '''Replaces existing item with new item'''
        cosmosclient, coll = SetupCosmosDB()
        #options = {"enableCrossPartitionQuery": True}
        #options['partitionKey'] = partitionid
        #options = {"partitionKey": ""}
        #options = { 'accessCondition' : { 'type': 'IfMatch', 'condition': etag } }
        try:
                resultreturn = cosmosclient.ReplaceItem(documentlink,newdocument)
        except:
                raise Exception
        return resultreturn
 