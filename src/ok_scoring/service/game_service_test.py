import unittest

from ok_scoring.model.game_rules import GameRules
from ok_scoring.model.player_score_history import PlayerScoreHistory
from ok_scoring.repository.helpers import unique_id
from ok_scoring.service.game_service import can_add_player_round, create_game


class TestCanAddPlayerRound(unittest.TestCase):
    def test_cannot_add_score_for_non_player_no_rules(self):
        player_score_history_one = PlayerScoreHistory(
            key='one',
            scores=[1, 3, -2],
            currentScore=1,
            playerKey='1',
            gameKey='1'
        )
        assert can_add_player_round(
            scoreHistory=player_score_history_one,
            playerKey='two',
            score=6,
            rules=None
        ) is False

    def test_can_add_score_for_player_no_rules(self):
        player_score_history_one = PlayerScoreHistory(
            key='one',
            scores=[1, 3, -2],
            currentScore=1,
            playerKey='1',
            gameKey='1'
        )
        assert can_add_player_round(
            scoreHistory=player_score_history_one,
            playerKey='one',
            score=6,
            rules=None
        ) is True


class TestCreateGame(unittest.TestCase):
    def test_can_create_game_with_description_only(self):
        game = create_game('Peanuts')
        assert game.description == 'Peanuts'
        assert game.key is not None
        assert game.date is not None
        assert game.duration is None
        assert game.winningPlayerKey is None
        assert game.scoreHistory == dict()
        assert game.scores == set()
        assert game.rules is None

    def test_can_create_game_with_description_and_players(self):
        player_key_1 = unique_id()
        game = create_game('Peanuts', [player_key_1])
        expected_score_history = dict()
        expected_score_history[player_key_1] = None
        assert game.description == 'Peanuts'
        assert game.key is not None
        assert game.date is not None
        assert game.duration is None
        assert game.winningPlayerKey is None
        assert game.scoreHistory is not None
        assert player_key_1 in game.scoreHistory
        assert game.scoreHistory[player_key_1].currentScore == 0
        assert game.scores == set()
        assert game.rules is None

    def test_can_create_game_with_description_players_and_rules(self):
        player_key_1 = unique_id()
        game_rules = GameRules(
            key=unique_id(),
            startingScore=100
        )
        game = create_game('Peanuts', [player_key_1], game_rules)
        expected_score_history = dict()
        expected_score_history[player_key_1] = None
        assert game.description == 'Peanuts'
        assert game.key is not None
        assert game.date is not None
        assert game.duration is None
        assert game.winningPlayerKey is None
        assert game.scoreHistory is not None
        assert player_key_1 in game.scoreHistory
        assert game.scoreHistory[player_key_1].currentScore == 100
        assert game.scores == set()
        assert game.rules is game_rules


if __name__ == '__main__':
    unittest.main()
