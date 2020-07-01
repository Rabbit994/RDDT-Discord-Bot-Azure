import requests

class TwitchAPI:
    
    def __init__(self,clientid:str,clientsecret:str):
        self.accesstoken = __get_access_token(clientid,clientsecret)
        self.clientid = clientid
    def __get_streams_by_userid(self,userid:str) -> dict:
        pass

    def __get_streams_by_userlogin(self,userlogin:str) -> dict:
        pass
    
    def __get_access_token(self,clientid:str,clientsecret:str) -> str:
        uri = f"https://id.twitch.tv/oauth2/token?client_id={clientid}" \
            f"&client_secret={clientsecret}&grant_type=client_credentials"
        r = requests.post(url=uri)
        accesstoken = r.json()
        accesstoken = accesstoken['access_token']