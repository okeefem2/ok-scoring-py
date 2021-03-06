from model.gameRules import GameRules
from repository.abstractRepository import AbstractRepository


class GameRulesRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, batch):
        self.session.add(batch)

    def get(self, reference):
        return self.session.query(GameRules).filter_by(reference=reference).one()

    def list(self):
        return self.session.query(GameRules).all()
