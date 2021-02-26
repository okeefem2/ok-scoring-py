from model.game_rules import GameRules
from model.player_score_history import PlayerScoreHistory
from service.game_service import can_add_player_round


class Game:
    scoreHistory: dict[str, PlayerScoreHistory]
    rules: GameRules

    def __init__(self, scoreHistory, rules=None):
        self.scoreHistory = scoreHistory
        self.rules = rules


    def add_player_round(self, playerKey: str, score: int):
        if can_add_player_round(self, playerKey, score):
            self.scoreHistory[playerKey].set_round_score(score)