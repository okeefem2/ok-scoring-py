
from ok_scoring.model.player_score_history import PlayerScoreHistory
from ok_scoring.repository.abstract_repository import AbstractRepository


class PlayerScoreHistoryRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, playerScoreHistory):
        self.session.add(playerScoreHistory)

    def get(self, key):
        return self.session.query(PlayerScoreHistory).filter_by(key=key).first()

    def get_player_scores_by_game_key(self, player_key, game_key):
        results = self.session.query(PlayerScoreHistory)\
            .filter_by(gameKey=game_key, playerKey=player_key).first()
        return results

    def list(self):
        return self.session.query(PlayerScoreHistory).all()

    def delete(self, key):
        playerScoreHistory = self.get(key)
        if playerScoreHistory is not None:
            self.session.delete(playerScoreHistory)
        else:
            return None

