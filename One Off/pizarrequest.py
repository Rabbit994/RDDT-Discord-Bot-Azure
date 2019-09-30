import Modules.DiscordFramework as DiscordFramework

results = DiscordFramework.get_member_list("414198832092545037")
totalusers = 0
usersinclan = 0
roleid = '414556877679230976' #This needs to be str
while len(results) == 1000:
    for result in results:
        totalusers += 1
        if roleid in result['roles']:
            usersinclan += 1
            if result['nick'] is None:
                nick = result['user']['username']
            else:
                nick = result['nick']
            print("{0} - DiscordID: {1}".format(nick,result['user']['id']))
    nextid = results[999]['user']['id']
    results = DiscordFramework.get_member_list("414198832092545037",after=nextid)
#After 1000 users, finish it off
for result in results:
        totalusers += 1
        if roleid in result['roles']:
            usersinclan += 1
            if result['nick'] is None:
                nick = result['user']['username']
            else:
                nick = result['nick']
            print("{0} - DiscordID: {1}".format(nick,result['user']['id']))

print("Total People in clan: {0}".format(usersinclan))
print("Total People in Discord: {0}".format(totalusers))