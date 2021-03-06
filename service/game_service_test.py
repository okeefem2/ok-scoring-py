import unittest

from model.game import Game
from model.playerScoreHistory import PlayerScoreHistory
from service.game_service import can_add_player_round


class TestCanAddPlayerRound(unittest.TestCase):
    def test_cannot_add_score_for_non_player_no_rules(self):
        player_score_history_one = PlayerScoreHistory(key='one', scores=[1, 3, -2], currentScore=1)
        game = Game(scoreHistory={'one': player_score_history_one})
        assert can_add_player_round(game, 'two', 6) is False

    def test_can_add_score_for_player_no_rules(self):
        player_score_history_one = PlayerScoreHistory(key='one', scores=[1, 3, -2], currentScore=1)
        game = Game(scoreHistory={'one': player_score_history_one})
        assert can_add_player_round(game, 'one', 6) is True


if __name__ == '__main__':
    unittest.main()
