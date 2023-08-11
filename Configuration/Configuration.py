from download_matches.Match_recuperation.faceit_api.faceit_data import FaceitData
import yaml
from yaml.loader import SafeLoader
import sys

class Configuration:
    def __init__(self):
        with open("./configuration.yaml", "r") as ymlfile:
            self.cfg = yaml.load(ymlfile, Loader=SafeLoader)

        print("configuration loaded")
        self.player_id = self.__get_player_id()
        self.demo_path = "demo_csgo/"

    def get(self, *keys):
        values = self.cfg
        for key in keys:
            values = values.get(key)
            if values is None:
                print('Key', key, 'not found')
                sys.exit()

        return values
    
    def __get_player_id(self):
        faceit_data = FaceitData(self.cfg['api']['key'])
        player = faceit_data.player_details(nickname=self.cfg['player']['name'])
        print(self.cfg["player"]["name"] + " player id: " + player["player_id"])

        return player["player_id"]