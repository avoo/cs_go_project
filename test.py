from Match_recuperation.Data_Parse import *
from faceit_api.faceit_data import FaceitData
from oppenent_analysis import *

player_name = "memetiti"
map_select = "de_overpass"

match_recuperation_dict_txt(api_key="38b28095-4ca6-48b6-aec5-748f507d5fcf",
                            player_id="57c4c556-3b8e-4695-bf55-122dde5040db", starting_item_position_call=0,
                            return_items_call=30, map_select=map_select, nickname = player_name )

print("map:",map_select,"team :",player_name)
print(gunround_T_analysis(player_name,map_select))