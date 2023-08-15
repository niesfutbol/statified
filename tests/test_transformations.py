import pandas as pd
import statified_nies as dt


def test_add_offset():
    augend = 1
    addend = 2
    expected = augend + addend
    obtained = dt.add_offset(augend, addend)
    assert expected == obtained


ws_players = pd.read_csv("static/larga_player.csv")
as_players = pd.read_csv("static/played_minutes_94.csv")


def test_list_of_players_in_ws_and_as():
    players = dt.list_of_players_in_ws_and_as(ws_players, as_players)
    expected_n = 243
    obtained_n = len(players)
    assert obtained_n == expected_n
