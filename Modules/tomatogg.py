import requests
import os

class TomatoGG:
    def __generate_header(self):
        header = {"User-Agent": "RDDT Discord Bot Contact: Rabbit#5740"}

    def get_user_info(self, wgid:int):
        uri = f"https://tomatobackend.herokuapp.com/api/abcd/com/{wgid}"
        try:
            r = requests.get(url=uri, headers = self.__generate_header())
            if r.status_code != 200:
                r = requests.get(url=uri, headers = self.__generate_header())
            return r.json()
        except:
            return None

