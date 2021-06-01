import unittest

from ok_scoring.model.player_score_history import PlayerScoreHistory
from ok_scoring.service.player_score_history_service import set_round_score


class TestSetRoundScore(unittest.TestCase):
    def test_adding_round_score_updates_current_score(self):
        player_score_history_one = PlayerScoreHistory(
            key='one',
            scores=[1, 3, -2],
            currentScore=1,
            playerKey='1',
            gameKey='1',
            order=0
        )
        set_round_score(player_score_history_one, 6, 3)
        assert player_score_history_one.currentScore == 8

        set_round_score(player_score_history_one, -10, 4)
        assert player_score_history_one.currentScore == -2

    def test_adding_round_score_beyond_last_index(self):
        player_score_history_one = PlayerScoreHistory(
            key='one',
            scores=[1, 3, -2],
            currentScore=1,
            playerKey='1',
            gameKey='1',
            order=0
        )
        set_round_score(player_score_history_one, 6, 5)
        assert player_score_history_one.currentScore == 8
        assert player_score_history_one.scores == [1, 3, -2, 0, 0, 6]

    def test_adding_round_score_idempotent(self):
        player_score_history_one = PlayerScoreHistory(
            key='one',
            scores=[1, 3, -2],
            currentScore=1,
            playerKey='1',
            gameKey='1',
            order=0
        )
        set_round_score(player_score_history_one, 6, 3)
        assert player_score_history_one.currentScore == 8
        assert player_score_history_one.scores == [1, 3, -2, 6]

        set_round_score(player_score_history_one, 6, 3)
        assert player_score_history_one.currentScore == 8
        assert player_score_history_one.scores == [1, 3, -2, 6]


if __name__ == '__main__':
    unittest.main()
