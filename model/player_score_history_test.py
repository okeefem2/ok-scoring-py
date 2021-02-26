import unittest

from model.player_score_history import PlayerScoreHistory


class TestSetRoundScore(unittest.TestCase):
    def test_adding_round_score_updates_current_score(self):
        player_score_history_one = PlayerScoreHistory(key='one', scores=[1, 3, -2], currentScore=1)
        player_score_history_one.set_round_score(6, 3)
        assert player_score_history_one.currentScore == 8

        player_score_history_one.set_round_score(-10, 4)
        assert player_score_history_one.currentScore == -2

    def test_adding_round_score_beyond_last_index(self):
        player_score_history_one = PlayerScoreHistory(key='one', scores=[1, 3, -2], currentScore=1)
        player_score_history_one.set_round_score(6, 5)
        assert player_score_history_one.currentScore == 8
        assert player_score_history_one.scores == [1, 3, -2, 0, 0, 6]

    def test_adding_round_score_idempotent(self):
        player_score_history_one = PlayerScoreHistory(key='one', scores=[1, 3, -2], currentScore=1)
        player_score_history_one.set_round_score(6, 3)
        assert player_score_history_one.currentScore == 8
        assert player_score_history_one.scores == [1, 3, -2, 6]

        player_score_history_one.set_round_score(6, 3)
        assert player_score_history_one.currentScore == 8
        assert player_score_history_one.scores == [1, 3, -2, 6]



if __name__ == '__main__':
    unittest.main()
