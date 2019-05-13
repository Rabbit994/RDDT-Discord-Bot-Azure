import json
import MySQLdb
import Frameworks.CommonFramework as CommonFramework
import Frameworks.CosmosFramework as CosmosFramework
import time

mysqlcinfo = CommonFramework.RetrieveConfigOptions("mysql")
mysqlconn = MySQLdb.connect(host=mysqlcinfo['server'],user=mysqlcinfo['username'],passwd=mysqlcinfo['password'],db=mysqlcinfo['database'])
mysqlconn.autocommit(True)
mysqlcur = mysqlconn.cursor()
cmd = "SELECT discordid,wgid,clan,rank,wgtoken,updated FROM users"
mysqlcur.execute(cmd)
data = mysqlcur.fetchall()
discordserverid = CommonFramework.RetrieveConfigOptions('discord')
discordserverid = discordserverid['discordserverid']
#Upload Users
for row in data:
    csdbdoc = dict()
    csdbdoc['discordid'] = str(row[0])
    csdbdoc['wgid'] = row[1]
    csdbdoc['clan'] = row[2]
    csdbdoc['rank'] = row[3]
    csdbdoc['wgtoken'] = str(row[4])
    csdbdoc['server'] = 'NA'
    csdbdoc['discordserverid'] = str(discordserverid)
    CosmosFramework.InsertItem(csdbdoc)
    time.sleep(.03)

#Upload Rank info
cmd = "SELECT discordid,wotclan,wotrank from discordroles"
mysqlcur.execute(cmd)
data = mysqlcur.fetchall()
for row in data:
    csdbdoc = dict()
    csdbdoc['discordid'] = str(row[0])
    csdbdoc['wotclan'] = row[1]
    csdbdoc['wotrank'] = row[2]
    csdbdoc['discordserverid'] = discordserverid
    csdbdoc['wotserver'] = 'NA'
    csdbdoc['role'] = 1
    CosmosFramework.InsertItem(csdbdoc)
    time.sleep(.03)