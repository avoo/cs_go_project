from flask import Flask

# from redis import Redis, RedisError
import os
import socket
from cs_go_analyse.opponent_analysis import *

# Connect to Redis
# redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)
player_name = "NENEs"
map_select = "de_inferno"

list_match = read_all_csgo_match_of_one_map_json(map_select)
df, data_player_t = pistol_analysis(player_name, map_select, list_match, side="t")
# df,data_player_ct,data_grenade_ct = pistol_analysis(player_name,map_select,list_match,side = 'ct')
Team_info = fav_bomb_site_analysis(player_name, list_match, map_select)


@app.route("/")
def hello():
    # df = pistol_analysis(player_name,map_select,list_match,side = 'ct',frame = 7)
    return (
        f"<h3>Analyse du joueur GiM6!</h3>"
        f"<b>Map analyser:</b> {map_select}<br/>"
        f"<b>Style de jeu:</b> {Team_info} <br/>"
        f"<img src='data:image/png;base64,{data_player_t}'/>"
    )
    # f"<img src='data:image/png;base64,{data_player_ct}'/>"\
    # f"<img src='data:image/png;base64,{data_grenade_ct}'/>"\
    # f"<p>More info à venir</p>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
