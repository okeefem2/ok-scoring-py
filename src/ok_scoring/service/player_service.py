from ok_scoring.model.player import Player
from ok_scoring.repository.helpers import unique_id


def create_player(name: str) -> Player:
    return Player(key=unique_id(), name=name, favorite=False)


def create_players(names: [str]) -> [Player]:
    return [create_player(name) for name in names]
