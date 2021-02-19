"""
This is check for Wargaming NA Stream and posting if active
"""
import time

from Modules.twitch import TwitchAPI
import Modules.CommonFramework as CommonFramework
import Modules.DiscordFramework as DiscordFramework

i = 0
channelid = '414607006821777440'
options = CommonFramework.RetrieveConfigOptions("twitch")
twitch = TwitchAPI(options['clientid'],options['clientsecret'])
users = ['worldoftanksna']
active = {}
for user in users:
    active[user] = False
while i < 1008:
    for user in users:
        currentstreams = twitch.get_streams_by_userlogin(userlogin=user)
        if len(currentstreams['data']) > 0 and active[user] is False:
            embed = {"title": f"Twitch Streamer {user} is active"}
            embed['type'] = 'rich'
            title = currentstreams['data'][0]['title']
            embed['description'] = f"Twitch Stream {user} is currently active and streaming {title}"
            embed['url'] = f"https://www.twitch.tv/{user}"
            DiscordFramework.SendDiscordMessage(message=None,channelid=channelid,embed=embed)
            active[user] = True
        elif len(currentstreams['data']) == 0 and active[user] is True:
            active[user] = False 
    i += 1 
    time.sleep(600)