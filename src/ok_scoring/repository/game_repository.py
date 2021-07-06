
from ok_scoring.model.game import Game
from ok_scoring.repository.abstract_repository import AbstractRepository


class GameRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, game):
        self.session.add(game)

    def get(self, key):
        return self.session.query(Game).filter_by(key=key).first()

    def list(self):
        return self.session.query(Game).all()

    def delete(self, key):
        game = self.get(key)
        if game is not None:
            self.session.delete(game)
        else:
            return None

    def update(self, entity):
        return self.session.update(entity)
