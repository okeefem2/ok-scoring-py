from src.model.gameRules import GameRules
from src.repository.abstractRepository import AbstractRepository


class GameRulesRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, batch):
        self.session.add(batch)

    def get(self, key):
        return self.session.query(GameRules).filter_by(key=key).one()

    def list(self):
        return self.session.query(GameRules).all()

    def delete(self, key):
        gameRules = self.get(key)
        if gameRules is not None:
            self.session.delete(gameRules)
        else:
            # TODO not found error

