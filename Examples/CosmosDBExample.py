import Frameworks.CommonFramework as CommonFramework
import Frameworks.CosmosFramework as CosmosFramework

'''This Example application is showing how using CosmosFramework to create a document,
query for documents, edit a document and delete a document for Cosmos DB in SQL API
Couple of things about Cosmos DB from someone who is used to more traditional databases, it's unstructured, 
meaning documents are not required to have similar fields, nor does must any field be unique
It's query language only supports SELECT, Insert/Update/Delete must be done via HTTP (handled by Framework)
Documents are CosmosDB equivalent of rows

For this example, I recommend download Microsoft Storage Explorer (https://azure.microsoft.com/en-us/features/storage-explorer/), or following along 
in Azure Portal which has web view of CosmosDB. THis is why example pauses after every change to let you see how it's working.
Remember your parameters.json file must exist with Document URL, Primary Key, Database (create in Azure Portal), Collection (create in Azure Portal)'''

#Create Document (discordid is partition Key for Cosmos DB in this example)
cosmosdoc = dict() #Make a dictionary to hold document
cosmosdoc['discordid'] = 12345
cosmosdoc['username'] = 'JohnDoe'
cosmosdoc['role'] = 'user'
CosmosFramework.InsertItem(cosmosdoc)
input("Press any key to continue")
#Retrieve Document inserted
results = CosmosFramework.QueryItems("SELECT * FROM c WHERE c.discordid = 12345")
print(results)
input("Press any key to continue")
#Results will return list of dict

#Edit item retrieved
editresult = results[0] #Putting first return from results into seperate dict
editresult['role'] = 'superuser'
editresult['clan'] = 'Awesome Clan' #Adding entry for user that didn't exist
neweditresult = CosmosFramework.ReplaceItem(editresult['_self'],editresult) #So Cosmos wants to know document to replace, all results have _self return which contains link to document
input("Press any key to continue")

#Delete item inserted
CosmosFramework.RemoveItem(neweditresult['_self'],neweditresult['discordid']) #So again, CosmosDB wants _self ID so it knows what to delete, it also prefers partitionKey for document
print("Deleted Submitted")

#Select for deleted record
results = CosmosFramework.QueryItems("SELECT * FROM c WHERE c.discordid= 12345")
if not results: #Meaning Results is empty
    print("Record Deleted")
else: #Well, that wasn't expected
    print("Delete not processed or more then one record exists for that Discordid")

