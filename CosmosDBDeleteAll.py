import Frameworks.CommonFramework as CommonFramework
import Frameworks.CosmosFramework as CosmosFramework
import time

results = CosmosFramework.QueryItems("SELECT * FROM c")
i = 0
for result in results:
    i += 1
    CosmosFramework.RemoveItem(result['_self'],result['discordid'])
    print("Deleting {0} row out {1}".format(i,len(results)))
    time.sleep(.1)
