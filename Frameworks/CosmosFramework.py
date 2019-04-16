import azure.cosmos.cosmos_client as cosmos_client
import Frameworks.CommonFramework as CommonFramework

def QueryCosmosDB(cosmosdbquery):
        '''Queries CosmosDB and returns results.'''
        config = CommonFramework.RetrieveConfigOptions("cosmosdb")
        cosmosclient = cosmos_client.CosmosClient(url_connection=config['ENDPOINT'],auth={'masterKey': config['PRIMARYKEY']})
        db = next((data for data in cosmosclient.ReadDatabases() if data['id'] == config['DATABASE']))
        coll = next((coll for coll in cosmosclient.ReadContainers(db['_self']) if coll['id'] == config['CONTAINER']))
        query = {'query': str(cosmosdbquery)}
        options = {"enableCrossPartitionQuery": True}
        resultreturn = cosmosclient.QueryItems(coll['_self'],query,options)
        results = list(resultreturn)
        return results
        