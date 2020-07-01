"""
This is check for Wargaming NA Stream and posting if active"""

from Modules import CommonFramework
import time

from Modules.twitch import TwitchAPI
import Modules.CosmosFramework as CosmosFramework
import Modules.wotframework as wotframework
import Modules.DiscordBotFramework as DiscordBotFramework
import Modules.CommonFramework as CommonFramework

options = CommonFramework.RetrieveConfigOptions("twitch")
twitch = TwitchAPI(options['clientid'],options['clientsecret'])
active = False #set to true if active and stream posted
while True:
    
    currentstreams = twitch.get_streams_by_userlogin(userlogin="worldoftanksna")
    if currentstreams['data']
    time.sleep(300)