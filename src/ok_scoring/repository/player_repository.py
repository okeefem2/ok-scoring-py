from ok_scoring.model.player import Player
from ok_scoring.model.player_score_history import PlayerScoreHistory
from ok_scoring.repository.abstract_repository import AbstractRepository


class PlayerRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def bulk_add(self, players):
        self.session.bulk_save_objects(players)

    def add(self, player):
        self.session.add(player)

    def get(self, key):
        return self.session.query(Player).filter_by(key=key).first()

    def get_by_name(self, name):
        return self.session.query(Player).filter_by(name=name).first()

    def get_by_names(self, names):
        return self.session.query(Player).filter(Player.name.in_(names)).all()

    def get_by_game_key(self, game_key):
        results = self.session.query(Player).join(PlayerScoreHistory)\
            .filter_by(gameKey=game_key).all()
        return results

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
