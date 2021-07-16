from ok_scoring.model.player import Player
from ok_scoring.model.validation_error import ValidationError
from ok_scoring.repository.helpers import unique_id


class NameRequired(ValidationError):
    pass


def build_new_player(name: str) -> Player:
    if name is None:
        raise NameRequired(
            propertyPath='player.name',
            errorType='required',
            errorMessage='Player name is required'
        )
    return Player(key=unique_id(), name=name, favorite=False)


def create_players(names: [str]) -> [Player]:
    players = []
    for name in names:
        player = build_new_player(name)
        players.append(player)
    return players


def filter_out_existing_names(players, names):
    if players is None or len(players) == 0:
        return names
    return list(filter(lambda name: all(player.name != name for player in players), names))
