
from ok_scoring.model.player_score_history import PlayerScoreHistory
from ok_scoring.repository.abstract_repository import AbstractRepository


class PlayerScoreHistoryRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, playerScoreHistory):
        self.session.add(playerScoreHistory)

    def get(self, key):
        return self.session.query(PlayerScoreHistory).filter_by(key=key).one()

    def list(self):
        return self.session.query(PlayerScoreHistory).all()

    def delete(self, key):
        playerScoreHistory = self.get(key)
        if playerScoreHistory is not None:
            self.session.delete(playerScoreHistory)
        else:
            return None

    def update(self, playerScoreHistory):
        return self.session.update(playerScoreHistory)
