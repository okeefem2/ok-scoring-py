from ok_scoring.model.player import Player
from ok_scoring.repository.abstract_repository import AbstractRepository
from ok_scoring.repository.helpers import unique_id


def create_player(name: str) -> Player:
    return Player(key=unique_id(), name=name, favorite=False)


def create_players(repo: AbstractRepository, session, names: [str]) -> [Player]:
    players = []
    for name in names:
        player = create_player(name)
        players.append(player)
        repo.add(player) # TODO maybe bulk add?
    session.commit()
    return players
