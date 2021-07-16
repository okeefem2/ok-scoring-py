import unittest

from ok_scoring.model.player_score_history import PlayerScoreHistory
from ok_scoring.service.player_score_history_service import set_round_score, is_current_round


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


class TestIsCurrentROund(unittest.TestCase):

    def test_current_round(self):
        player_score_history_one = PlayerScoreHistory(
            key='one',
            scores=[1, 3, -2],
            currentScore=1,
            playerKey='1',
            gameKey='1',
            order=0
        )
        player_score_history_two = PlayerScoreHistory(
            key='two',
            scores=[1, 3],
            currentScore=1,
            playerKey='2',
            gameKey='1',
            order=0
        )

        score_history = [player_score_history_one, player_score_history_two]

        assert is_current_round(score_history, 2) is True

if __name__ == '__main__':
    unittest.main()
