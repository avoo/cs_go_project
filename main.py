# # CS GO DOWNLOAD AND PARSE
#
# # I/ PARSE
#
# #### Mandatory : Enter the player_name of one of your opponent and the map on which you are going to play.
# #### Optional : Enter the list of several opponents so you will analyze only matches with the same premade.

from cs_go_analyse.opponent_analysis import *
import pandas as pd
from download_matches.Match_recuperation.Demo import *
from Configuration.Configuration import *
import pandas as pd
import sys

if __name__ == "__main__":
    config = Configuration()
    demo = Demo(config)

    # TODO replace variables by the configuration
    player_name = config.get('player', 'name')
    map_select = config.get('map')
    premade = config.get('player', 'premade')

    demo.download_and_parse(
        starting_item_position_call=0,
        return_items_call=70,
        map_select=map_select,
        premade=premade,
        replace=True,
        nb_match_analyses_max=10,
    )

    # # II/ Match Analysis
    #
    # ## A/ Gameplay general style analysis

    list_match = demo.read_all_csgo_match_of_one_map_json()

    data, df = fav_bomb_site_analysis(player_name, list_match, map_select)

    print("", data, "")

    # # B/ Gunround and following round analysis
    # ## B.1/ T side pistol

    print("SIDE = T, map:", map_select, "team :", player_name)
    df = pistol_analysis(player_name, map_select, list_match, side="t")

    second_round(
        player_name, map_select, list_match, side="t", premade=[], winning_gr_side="T"
    )

    second_round(
        player_name, map_select, list_match, side="t", premade=[], winning_gr_side="CT"
    )

    # ### B.2/ CT side pistol

    pd.set_option("display.max_rows", 500)
    print("SIDE = CT, map:", map_select, "team :", player_name)
    df, df4 = ct_positionement_start(
        player_name, map_select, list_match, frame=7, buy_type="Pistol Round"
    )
    display(df)
    df = pistol_analysis(player_name, map_select, list_match, side="ct", start_frame=7)
    df[0]

    second_round(
        player_name, map_select, list_match, side="ct", premade=[], winning_gr_side="CT"
    )

    second_round(
        player_name, map_select, list_match, side="ct", premade=[], winning_gr_side="T"
    )

    # ### CT killer position fav

    ct_kill_position(player_name, map_select, list_match, ["Parfell"])

    # ## C/ CT side All type of rounds analysis (full buy vs semi buy etc)
    # ### C.1/ CT Full buy analysis

    print("SIDE = T, map:", map_select, "team :", player_name)
    df = ct_positionement_start(
        player_name, map_select, list_match, frame=7, buy_type="Full Buy"
    )
    display(df)
    # df = round_analysis(player_name,map_select,list_match,side = 'ct',premade = [],frame = 7)
    for player in premade:
        df = round_analysis(
            player_name, map_select, list_match, side="ct", premade=[player], frame=7
        )

    # ### C.2/ CT Semi Buy analysis

    print("SIDE = T, map:", map_select, "team :", player_name)
    df = ct_positionement_start(
        player_name, map_select, list_match, frame=7, buy_type="Semi Buy"
    )
    display(df)
    df = round_analysis(
        player_name, map_select, list_match, side="ct", premade=[], buy_type="Semi Buy"
    )
    for player in premade:
        df = round_analysis(
            player_name,
            map_select,
            list_match,
            side="ct",
            premade=[player],
            buy_type="Semi Buy",
        )

    # ### C.3/ CT Semi Eco analysis

    print("SIDE = T, map:", map_select, "team :", player_name)
    df = ct_positionement_start(
        player_name, map_select, list_match, frame=7, buy_type="Semi Eco"
    )
    display(df)
    df = round_analysis(
        player_name, map_select, list_match, side="ct", premade=[], buy_type="Semi Eco"
    )
    for player in premade:
        df = round_analysis(
            player_name,
            map_select,
            list_match,
            side="ct",
            premade=[player],
            buy_type="Semi Eco",
        )

    # ### C.4/ CT Full Eco analysis

    print("SIDE = T, map:", map_select, "team :", player_name)
    df = ct_positionement_start(
        player_name, map_select, list_match, frame=7, buy_type="Full Eco"
    )
    display(df)
    df = round_analysis(
        player_name, map_select, list_match, side="ct", premade=[], buy_type="Full Eco"
    )
    for player in premade:
        df = round_analysis(
            player_name,
            map_select,
            list_match,
            side="ct",
            premade=[player],
            buy_type="Full Eco",
        )

    # ## D/ T side all rounds analysis
    # ### D.1/ T full buy analysis

    print("SIDE = T, map:", map_select, "team :", player_name)
    # round_analysis(player_name,map_select,list_match,side = 't',premade = [])
    for player in premade:
        df = round_analysis(
            player_name, map_select, list_match, side="t", premade=[player]
        )

    # ### D.2/ T Semi Buy analysis

    df = round_analysis(
        player_name, map_select, list_match, side="t", premade=[], buy_type="Semi Buy"
    )
    for player in premade:
        df = round_analysis(
            player_name,
            map_select,
            list_match,
            side="t",
            premade=[player],
            buy_type="Semi Buy",
        )

    # ### D.3/ T Semi Eco analysis

    df = round_analysis(
        player_name, map_select, list_match, side="t", premade=[], buy_type="Semi Eco"
    )
    for player in premade:
        df = round_analysis(
            player_name,
            map_select,
            list_match,
            side="t",
            premade=[player],
            buy_type="Semi Eco",
        )

    # ### D.4/ T Full Eco analysis

    df = round_analysis(
        player_name, map_select, list_match, side="t", premade=[], buy_type="Full Eco"
    )
    for player in premade:
        df = round_analysis(
            player_name,
            map_select,
            list_match,
            side="t",
            premade=[player],
            buy_type="Full Eco",
        )
