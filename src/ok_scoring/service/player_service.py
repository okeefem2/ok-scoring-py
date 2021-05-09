from ok_scoring.model.player import Player
from ok_scoring.model.validation_error import ValidationError
from ok_scoring.repository.helpers import unique_id
from ok_scoring.repository.player_repository import PlayerRepository


class NameRequired(ValidationError):
    pass


def create_player(name: str) -> Player:
    if name is None:
        raise NameRequired('Player name is required')
    return Player(key=unique_id(), name=name, favorite=False)


def create_players(repo: PlayerRepository, names: [str]) -> [Player]:
    players = []
    for name in names:
        player = repo.get_by_name(name)
        if player is None:
            player = create_player(name)
            repo.add(player)  # TODO maybe bulk add?
        players.append(player)
    return players
