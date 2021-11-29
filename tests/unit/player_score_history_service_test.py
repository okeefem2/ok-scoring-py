import unittest

from ok_scoring.model.player_score_history import PlayerScoreHistory
from ok_scoring.model.score_round import ScoreRound
from ok_scoring.service.player_score_history_service import set_round_score, is_current_round, calculate_current_score, \
    is_round_complete, find_by_order_index, find_by_player_key, build_score_history, build_player_score_history, \
    PlayerKeyRequired, GameKeyRequired, OrderRequired, calculate_round_score


class TestSetRoundScore(unittest.TestCase):

    def test_adding_round_score_updates_current_score(self):
        round_one = ScoreRound(scores=[1], roundScore=1, key='1', playerScoreHistoryKey='one', order=0)
        round_two = ScoreRound(scores=[3], roundScore=3, key='2', playerScoreHistoryKey='one', order=1)
        round_three = ScoreRound(scores=[-2], roundScore=-2, key='3', playerScoreHistoryKey='one', order=2)
        player_score_history_one = PlayerScoreHistory(
            key='one',
            scores=[round_one, round_two, round_three],
            currentScore=2,
            playerKey='1',
            gameKey='1',
            order=0
        )
        set_round_score(player_score_history_one, score=6, round_index=3, score_index=0)
        assert player_score_history_one.currentScore == 8

        set_round_score(player_score_history_one, score=-10, round_index=4, score_index=0)
        assert player_score_history_one.currentScore == -2

    def test_adding_round_score_beyond_last_index(self):
        round_one = ScoreRound(scores=[1], roundScore=1, key='1', playerScoreHistoryKey='one', order=0)
        round_two = ScoreRound(scores=[3], roundScore=3, key='2', playerScoreHistoryKey='one', order=1)
        round_three = ScoreRound(scores=[-2], roundScore=-2, key='3', playerScoreHistoryKey='one', order=2)
        player_score_history_one = PlayerScoreHistory(
            key='one',
            scores=[round_one, round_two, round_three],
            currentScore=2,
            playerKey='1',
            gameKey='1',
            order=0
        )
        set_round_score(player_score_history_one, score=6, round_index=5, score_index=0)
        assert player_score_history_one.currentScore == 8
        assert len(player_score_history_one.scores) == 6

    def test_adding_round_score_idempotent(self):
        round_one = ScoreRound(scores=[1], roundScore=1, key='1', playerScoreHistoryKey='one', order=0)
        round_two = ScoreRound(scores=[3], roundScore=3, key='2', playerScoreHistoryKey='one', order=1)
        round_three = ScoreRound(scores=[-2], roundScore=-2, key='3', playerScoreHistoryKey='one', order=2)
        player_score_history_one = PlayerScoreHistory(
            key='one',
            scores=[round_one, round_two, round_three],
            currentScore=2,
            playerKey='1',
            gameKey='1',
            order=0
        )
        set_round_score(player_score_history_one, score=6, round_index=3, score_index=0)
        assert player_score_history_one.currentScore == 8
        assert len(player_score_history_one.scores) == 4

        set_round_score(player_score_history_one, score=6, round_index=3, score_index=0)
        assert player_score_history_one.currentScore == 8
        assert len(player_score_history_one.scores) == 4

    def test_updating_score_in_round(self):
        round_one = ScoreRound(scores=[1], roundScore=1, key='1', playerScoreHistoryKey='one', order=0)
        round_two = ScoreRound(scores=[3, 2, -1], roundScore=4, key='2', playerScoreHistoryKey='one', order=1)
        round_three = ScoreRound(scores=[-2], roundScore=-2, key='3', playerScoreHistoryKey='one', order=2)
        player_score_history_one = PlayerScoreHistory(
            key='one',
            scores=[round_one, round_two, round_three],
            currentScore=3,
            playerKey='1',
            gameKey='1',
            order=0
        )
        set_round_score(player_score_history_one, score=6, round_index=1, score_index=1)
        assert player_score_history_one.currentScore == 7
        assert len(player_score_history_one.scores) == 3
        assert player_score_history_one.scores[1].roundScore == 8
        assert player_score_history_one.scores[1].scores[1] == 6


    def test_adding_score_in_round(self):
        round_one = ScoreRound(scores=[1], roundScore=1, key='1', playerScoreHistoryKey='one', order=0)
        round_two = ScoreRound(scores=[4], roundScore=4, key='2', playerScoreHistoryKey='one', order=1)
        round_three = ScoreRound(scores=[-2], roundScore=-2, key='3', playerScoreHistoryKey='one', order=2)
        player_score_history_one = PlayerScoreHistory(
            key='one',
            scores=[round_one, round_two, round_three],
            currentScore=3,
            playerKey='1',
            gameKey='1',
            order=0
        )
        set_round_score(player_score_history_one, score=6, round_index=1, score_index=1)
        assert player_score_history_one.currentScore == 9
        assert len(player_score_history_one.scores) == 3
        assert player_score_history_one.scores[1].roundScore == 10
        assert player_score_history_one.scores[1].scores[1] == 6


class TestCalculateRoundScore(unittest.TestCase):
    def test_no_round(self):
        assert calculate_round_score(None) is None

    def test_sums_round_scores(self):
        score_round = ScoreRound(scores=[-1, 2, 4, 0, -2], roundScore=0, key='1', playerScoreHistoryKey='one', order=0)
        score_round = calculate_round_score(score_round)
        assert score_round.roundScore == 3


class TestCalculateCurrentScore(unittest.TestCase):

    def test_no_rounds(self):
        assert calculate_current_score([]) == 0
        assert calculate_current_score(None) == 0

    def test_one_round(self):
        round_one = ScoreRound(scores=[1], roundScore=1, key='1', playerScoreHistoryKey='one', order=0)
        assert calculate_current_score([round_one]) == 1

    def test_multiple_round(self):
        round_one = ScoreRound(scores=[1], roundScore=1, key='1', playerScoreHistoryKey='one', order=0)
        round_two = ScoreRound(scores=[3, 2, -2], roundScore=3, key='2', playerScoreHistoryKey='one', order=1)
        round_three = ScoreRound(scores=[-2], roundScore=-2, key='3', playerScoreHistoryKey='one', order=2)
        assert calculate_current_score([round_one, round_two, round_three]) == 2


class TestBuildPlayerScoreHistory(unittest.TestCase):

    def test_with_default_values(self):
        player_score_history = build_player_score_history('1', '2', 0)

        assert player_score_history.playerKey == '1'
        assert player_score_history.gameKey == '2'
        assert player_score_history.order == 0
        assert player_score_history.scores == []
        assert player_score_history.currentScore == 0

    def test_with_starting_score(self):
        player_score_history = build_player_score_history('2', '4', 1, 10)

        assert player_score_history.playerKey == '2'
        assert player_score_history.gameKey == '4'
        assert player_score_history.order == 1
        assert player_score_history.scores == []
        assert player_score_history.currentScore == 10

    def test_with_scores(self):
        scores = [5, 6, -1]
        player_score_history = build_player_score_history('3', '5', 6, 10, scores)

        assert player_score_history.playerKey == '3'
        assert player_score_history.gameKey == '5'
        assert player_score_history.order == 6
        assert player_score_history.scores == scores
        assert player_score_history.currentScore == 10

    def test_no_player_key(self):
        self.assertRaises(PlayerKeyRequired, build_player_score_history, None, '1', 0)

    def test_no_game_key(self):
        self.assertRaises(GameKeyRequired, build_player_score_history, '1', None, 0)

    def test_no_order(self):
        self.assertRaises(OrderRequired, build_player_score_history, '1', '1', None)


class TestBuildScoreHistory(unittest.TestCase):

    def test_creates_empty_list_for_no_players(self):
        assert build_score_history([], '1') == []

    def test_creates_score_history_for_each_player(self):
        score_history = build_score_history(['1', '2'], '1')
        assert len(score_history) == 2


class TestFindByPlayerKey(unittest.TestCase):

    def test_no_players(self):
        assert find_by_player_key([], '1') is None
        assert find_by_player_key(None, '1') is None

    def test_no_player_with_key(self):
        player_score_history_one = PlayerScoreHistory(
            key='one',
            scores=[],
            currentScore=1,
            playerKey='1',
            gameKey='1',
            order=0
        )
        assert find_by_player_key([player_score_history_one], '2') is None

    def test_key_matches(self):
        player_score_history_one = PlayerScoreHistory(
            key='one',
            scores=[],
            currentScore=1,
            playerKey='1',
            gameKey='1',
            order=0
        )
        player_score_history_two = PlayerScoreHistory(
            key='two',
            scores=[],
            currentScore=1,
            playerKey='2',
            gameKey='1',
            order=1
        )
        score_history = [
            player_score_history_one,
            player_score_history_two
        ]
        assert find_by_player_key(score_history, '2') is player_score_history_two


class TestFindByOrderIndex(unittest.TestCase):

    def test_no_players(self):
        assert find_by_order_index([], 1) is None
        assert find_by_order_index(None, 1) is None

    def test_no_player_with_index(self):
        player_score_history_one = PlayerScoreHistory(
            key='one',
            scores=[],
            currentScore=1,
            playerKey='1',
            gameKey='1',
            order=0
        )
        assert find_by_order_index([player_score_history_one], 1) is None
    
    def test_index_matches_order(self):
        player_score_history_one = PlayerScoreHistory(
            key='one',
            scores=[],
            currentScore=1,
            playerKey='1',
            gameKey='1',
            order=0
        )
        player_score_history_two = PlayerScoreHistory(
            key='two',
            scores=[],
            currentScore=1,
            playerKey='2',
            gameKey='1',
            order=1
        )
        score_history = [
            player_score_history_one,
            player_score_history_two
        ]
        assert find_by_order_index(score_history, 1) is player_score_history_two


class TestIsCurrentRound(unittest.TestCase):

    def test_current_round(self):
        round_one = ScoreRound(scores=[1], roundScore=1, key='1', playerScoreHistoryKey='one', order=0)
        round_two = ScoreRound(scores=[3, 2, -2], roundScore=3, key='2', playerScoreHistoryKey='one', order=1)
        round_three = ScoreRound(scores=[-2], roundScore=-2, key='3', playerScoreHistoryKey='one', order=2)

        player_score_history_one = PlayerScoreHistory(
            key='one',
            scores=[round_one, round_two, round_three],
            currentScore=1,
            playerKey='1',
            gameKey='1',
            order=0
        )
        player_score_history_two = PlayerScoreHistory(
            key='two',
            scores=[round_one, round_two],
            currentScore=1,
            playerKey='2',
            gameKey='1',
            order=0
        )

        score_history = [player_score_history_one, player_score_history_two]

        assert is_current_round(score_history, 2) is True


class TestIsRoundComplete(unittest.TestCase):

    def test_round_complete(self):
        player_one_round_one = ScoreRound(scores=[1], roundScore=1, key='1', playerScoreHistoryKey='one', order=0)
        player_one_round_Two = ScoreRound(scores=[3], roundScore=3, key='2', playerScoreHistoryKey='one', order=1)
        player_score_history_one = PlayerScoreHistory(
            key='one',
            scores=[player_one_round_one, player_one_round_Two],
            currentScore=1,
            playerKey='1',
            gameKey='1',
            order=0
        )
        player_two_round_one = ScoreRound(scores=[1], roundScore=1, key='1', playerScoreHistoryKey='two', order=0)
        player_score_history_two = PlayerScoreHistory(
            key='two',
            scores=[player_two_round_one],
            currentScore=1,
            playerKey='2',
            gameKey='1',
            order=0
        )
        score_history = [
            player_score_history_one,
            player_score_history_two
        ]
        assert is_round_complete(score_history, 0) is True

    def test_round_incomplete(self):
        player_one_round_one = ScoreRound(scores=[1], roundScore=1, key='1', playerScoreHistoryKey='one', order=0)
        player_one_round_Two = ScoreRound(scores=[3], roundScore=3, key='2', playerScoreHistoryKey='one', order=1)
        player_score_history_one = PlayerScoreHistory(
            key='one',
            scores=[player_one_round_one, player_one_round_Two],
            currentScore=1,
            playerKey='1',
            gameKey='1',
            order=0
        )
        player_two_round_one = ScoreRound(scores=[1], roundScore=1, key='1', playerScoreHistoryKey='two', order=0)
        player_score_history_two = PlayerScoreHistory(
            key='two',
            scores=[player_two_round_one],
            currentScore=1,
            playerKey='2',
            gameKey='1',
            order=0
        )
        score_history = [
            player_score_history_one,
            player_score_history_two
        ]
        assert is_round_complete(score_history, 1) is False

    def test_no_players(self):
        score_history = []
        assert is_round_complete(score_history, 0) is False
        assert is_round_complete(None, 0) is False

    def test_no_rounds(self):
        player_score_history_one = PlayerScoreHistory(
            key='one',
            scores=[],
            currentScore=1,
            playerKey='1',
            gameKey='1',
            order=0
        )
        player_score_history_two = PlayerScoreHistory(
            key='two',
            scores=[],
            currentScore=1,
            playerKey='2',
            gameKey='1',
            order=0
        )
        score_history = [
            player_score_history_one,
            player_score_history_two
        ]
        assert is_round_complete(score_history, 0) is False


if __name__ == '__main__':
    unittest.main()
