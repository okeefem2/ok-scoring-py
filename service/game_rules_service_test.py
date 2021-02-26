import unittest

from model.game_rules import GameRules
from service.game_rules_service import validate_rounds, ExceededRounds, validate_score, ScoreBusts


class TestValidateRounds(unittest.TestCase):

    def test_can_add_score_for_player_under_round_cap(self):
        rules = GameRules(key="rules_one", rounds=5)
        assert validate_rounds(rules, 3) is True

    def test_can_add_score_for_player_meeting_round_cap(self):
        rules = GameRules(key="rules_one", rounds=4)
        assert validate_rounds(rules, 3) is True

    def test_cannot_add_score_for_player_at_round_cap(self):
        rules = GameRules(key="rules_one", rounds=3)
        self.assertRaises(ExceededRounds, validate_rounds, rules, 3)


class TestValidateScore(unittest.TestCase):
    def test_cannot_add_score_for_player_that_busts_positive(self):
        rules = GameRules(key="rules_one", canBust=True, winningScore=5, highScoreWins=True)
        self.assertRaises(ScoreBusts, validate_score, rules, 1, 6)

    def test_cannot_add_score_for_player_that_busts_negative(self):
        rules = GameRules(key="rules_one", canBust=True, winningScore=0, highScoreWins=False)
        self.assertRaises(ScoreBusts, validate_score, rules, 1, -6)


if __name__ == '__main__':
    unittest.main()
