import requests

class TwitchAPI:
    
    def __init__(self,clientid:str,clientsecret:str):
        self.accesstoken = self.__get_access_token(clientid,clientsecret)
        self.clientid = clientid

    #Public
    def get_streams_by_userlogin(self,userlogin:str) -> dict:
        uri = f"https://api.twitch.tv/helix/streams?user_login={userlogin}"
        headers = {"Authorization":f"Bearer {self.accesstoken}","Client-ID": self.clientid}
        r = requests.get(url=uri,headers=headers)
        return r.json()
    
    def get_streams_by_userid(self,userid:str) -> dict:
        uri = f"https://api.twitch.tv/helix/streams?user_id={userlogin}"
        headers = {"Authorization":f"Bearer {self.accesstoken}","Client-ID": self.clientid}
        r = requests.get(url=uri,headers=headers)
        return r.json()
        pass

    def __get_access_token(self,clientid:str,clientsecret:str) -> str:
        uri = f"https://id.twitch.tv/oauth2/token?client_id={clientid}" \
            f"&client_secret={clientsecret}&grant_type=client_credentials"
        r = requests.post(url=uri)
        accesstoken = r.json()
        accesstoken = accesstoken['access_token']
        return accesstoken

    
    #Private
    

    