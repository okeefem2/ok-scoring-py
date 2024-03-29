from ok_scoring.model.player import Player
from ok_scoring.model.validation_error import OKValidationError
from ok_scoring.repository.helpers import unique_id


class NameRequired(OKValidationError):
    pass


def build_new_player(name: str) -> Player:
    if name is None:
        raise NameRequired(
            propertyPath='player.name',
            errorType='required',
            errorMessage='Player name is required'
        )
    return Player(key=unique_id(), name=name, favorite=False)


def create_players(names: [str], existing_players: [Player]) -> [Player]:
    new_player_names = filter_out_existing_names(existing_players, names)
    return [build_new_player(name) for name in new_player_names]


def filter_out_existing_names(players, names):
    if players is None or len(players) == 0:
        return names
    return list(filter(lambda name: all(player.name != name for player in players), names))
