def add_offset(augend: int, addend: int) -> int:
    return augend + addend


def list_of_players_in_ws_and_as(longer, played_minutes):
    return [
        jugador
        for jugador in longer.Player.unique().tolist()
        if jugador in played_minutes.player.to_list()
    ]
