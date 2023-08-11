import os
from awpy.parser import DemoParser
from Configuration.Configuration import *
from .faceit_api.faceit_data import FaceitData
import requests
import re
import patoolib
import multiprocessing
from yaml.loader import SafeLoader
import yaml
import json
import sys
from typing import Type

class Demo:
    def __init__(self, configuration: Type[Configuration]):
        self.__config = configuration

    def download_and_parse(
        self,
        starting_item_position_call=0,
        return_items_call=2,
        map_select=None,
        premade=[],
        replace=False,
        nb_match_analyses_max=4,
    ):
        faceit_data = FaceitData(self.__config.get('api', 'key'))

        print("get matches from faceit")
        all_match_player = faceit_data.player_matches(
            player_id=self.__config.player_id,
            game="csgo",
            starting_item_position=starting_item_position_call,
            return_items=return_items_call,
        )

        proc = []
        succeed = 0
        cpt = 0
        if replace:
            print("removing old demos in", self.__config.demo_path + map_select, "###")
            filelist = [f for f in os.listdir(self.__config.demo_path + map_select) if f.startswith(self.__config.get('player', 'name'))]
            
            for f in filelist:
                os.remove(os.path.join(self.__config.demo_path + map_select, f))
        
        for i in range(len(all_match_player["items"])):
            cpt += 1
            #  try:
            match_detail = faceit_data.match_details(
                match_id=all_match_player["items"][i]["match_id"]
            )
            map = match_detail["voting"]["map"]["pick"][0]
            print(
                "_______________START DOWNLOADING MATCH NUMBER :",
                cpt,
                "on map :",
                map,
                "___SUCCEED BEFORE : ",
                succeed,
            )
            if (map_select != None) & (map != map_select):
                print("wrong map: ", map, "vs", map_select)
                continue

            cpt = 0
            nb_premade = len(premade)
            print("Check premade : ")
            for faction in ["faction1", "faction2"]:
                for roster in match_detail["teams"][faction]["roster"]:
                    if roster["nickname"] in premade:
                        print(roster["nickname"], " founded")
                        cpt += 1
            if cpt != nb_premade:
                print("###il manque :", nb_premade - cpt, " premade###")
                continue

            verif = 0
            faceit_data = FaceitData(self.__config.get('api', 'key'))
            print(all_match_player["items"][i]["match_id"])
            match_details = faceit_data.match_details(
                all_match_player["items"][i]["match_id"]
            )
            match_name = all_match_player["items"][i]["match_id"]

            for root, dirs, files in os.walk(
                self.__config.demo_path + match_details["voting"]["map"]["pick"][0]
            ):
                for filename in files:
                    if not filename.startswith(self.__config.get('player', 'name')):
                        continue

                    print(
                        filename,
                        " compare to : ",
                        self.__config.get('player', 'name')
                        + "_"
                        + match_details["voting"]["map"]["pick"][0]
                        + "_"
                        + str(match_details["configured_at"])
                        + "_"
                        + match_name
                        + ".txt",
                    )
                    if (
                        filename
                        == self.__config.get('player', 'name')
                        + "_"
                        + match_details["voting"]["map"]["pick"][0]
                        + "_"
                        + str(match_details["configured_at"])
                        + "_"
                        + match_name
                        + ".json"
                    ):
                        verif = 1
                        break
            print("nb_game_json:", succeed)

            if verif == 1:
                print("demo déjà présente, on passe à la suite")
                continue

            url = match_details["demo_url"][0]
            headers = {
                "accept": "application/json",
                "Authorization": "Bearer {}".format(self.__config.get('api', 'key')),
            }

            proc.append(
                multiprocessing.Process(
                    target=Demo(self.__config).parse_demos,
                    args=(url, match_details, all_match_player, self.__config.get('player', 'name'), i),
                )
            )
            proc[succeed].start()
            succeed += 1
            if succeed >= nb_match_analyses_max:
                print("Enough matches downloaded")
                break

        #  except:
        #      print("error before download and parse"
        # for proc1 in proc :
        #  proc1.start()
        print("En attente de FIN download and parse")
        print("succeed", succeed)
        for proc2 in proc:
            print("proc:", proc2)
            proc2.join()
        # b = multiprocessing.Barrier(succeed)
        # b.wait()
        print("DONE Doawnloading and parsing")

    def read_all_csgo_match_of_one_map_json(self):
        list_match = []
        print('Reading demos for', self.__config.get('map'))
        for root, dirs, files in os.walk(self.__config.demo_path + self.__config.get('map')):
            for filename in files:
                if not filename.startswith(self.__config.get('player', 'name')):
                    continue

                pattern = '(' + self.__config.get('player', 'name') + '_' + self.__config.get('map') + '.*?).json'
                filename = re.search(pattern, filename).group(1)

                with open(
                    self.__config.demo_path + self.__config.get('map') + "/" + filename + ".json"
                ) as file:
                    data = json.load(file)
                    list_match.append(data)

        return list_match

    def parse_demos(
        self,
        url,
        match_details,
        all_match_player,
        nickname,
         i
    ):
        #  try:
        print(url)
        r = requests.get(url)
        #  print(r.status_code)
        with open(
            self.__config.demo_path
            + match_details["voting"]["map"]["pick"][0]
            + "_"
            + str(match_details["configured_at"])
            + ".dem.7z",
            "wb",
        ) as f:
            f.write(r.content)
        print(
            self.__config.demo_path
            + match_details["voting"]["map"]["pick"][0]
            + "_"
            + str(match_details["configured_at"])
            + ".dem.7z"
        )

        patoolib.extract_archive(
            self.__config.demo_path
            + match_details["voting"]["map"]["pick"][0]
            + "_"
            + str(match_details["configured_at"])
            + ".dem.7z",
            outdir=self.__config.demo_path,
        )
        print("extract to:")
        s = match_details["demo_url"][0]
        pattern = "csgo/(.*?).dem"
        match_name = re.search(pattern, s).group(1)

        print(
            "debut du parse",
            self.__config.demo_path
            + match_details["voting"]["map"]["pick"][0]
            + "_"
            + str(match_details["configured_at"])
            + ".dem",
        )
        try:
            demo_parser = DemoParser(
                demofile=self.__config.demo_path
                + match_details["voting"]["map"]["pick"][0]
                + "_"
                + str(match_details["configured_at"])
                + ".dem",
                demo_id=nickname
                + "_"
                + match_details["voting"]["map"]["pick"][0]
                + "_"
                + str(match_details["configured_at"])
                + "_"
                + match_name,
                parse_rate=128,
                outpath=self.__config.demo_path
                + match_details["voting"]["map"]["pick"][0]
                + "/",
            )
            data = demo_parser.parse()
            os.remove(
                self.__config.demo_path
                + match_details["voting"]["map"]["pick"][0]
                + "_"
                + str(match_details["configured_at"])
                + ".dem"
            )
            os.remove(
                self.__config.demo_path
                + match_details["voting"]["map"]["pick"][0]
                + "_"
                + str(match_details["configured_at"])
                + ".dem.7z"
            )
        except:
            demo_parser = DemoParser(
                demofile=self.__config.demo_path + match_name + ".dem",
                demo_id=nickname
                + "_"
                + match_details["voting"]["map"]["pick"][0]
                + "_"
                + str(match_details["configured_at"])
                + "_"
                + match_name,
                parse_rate=128,
                outpath=self.__config.demo_path
                + match_details["voting"]["map"]["pick"][0]
                + "/",
            )
            data = demo_parser.parse()
            os.remove(self.__config.demo_path + match_name + ".dem")
            os.remove(
                self.__config.demo_path
                + match_details["voting"]["map"]["pick"][0]
                + "_"
                + str(match_details["configured_at"])
                + ".dem.7z"
            )
        print("parse success")

        print(
            match_details["voting"]["map"]["pick"][0]
            + "_"
            + str(match_details["configured_at"])
            + "_"
            + match_name
        )