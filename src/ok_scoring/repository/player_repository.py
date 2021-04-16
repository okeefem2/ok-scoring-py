
from ok_scoring.model.game import Game
from ok_scoring.model.player import Player
from ok_scoring.repository.abstract_repository import AbstractRepository


class PlayerRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, player):
        self.session.add(player)

    def get(self, key):
        return self.session.query(Player).filter_by(key=key).one()

    def list(self):
        return self.session.query(Player).all()

    def delete(self, key):
        player = self.get(key)
        if player is not None:
            self.session.delete(player)
        else:
            return None

    def update(self, entity):
        return self.session.update(entity)
