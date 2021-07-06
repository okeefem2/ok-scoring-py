
from ok_scoring.model.game_rules import GameRules
from ok_scoring.repository.abstract_repository import AbstractRepository


class GameRulesRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, batch):
        self.session.add(batch)

    def get(self, key):
        return self.session.query(GameRules).filter_by(key=key).first()

    def list(self):
        return self.session.query(GameRules).all()

    def delete(self, key):
        gameRules = self.get(key)
        if gameRules is not None:
            self.session.delete(gameRules)
        else:
            return None

    def update(self, entity):
        return self.session.update(entity)
