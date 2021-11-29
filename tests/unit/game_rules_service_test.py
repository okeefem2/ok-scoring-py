import unittest

from jsonschema_rs import ValidationError
from ok_scoring.model.game import Game
from ok_scoring.model.game_rules import GameRules
from ok_scoring.model.player_score_history import PlayerScoreHistory
from ok_scoring.model.score_round import ScoreRound
from ok_scoring.service.game_rules_service import validate_game_state, is_game_won
import json
import os


class ValidateGameStateTest(unittest.TestCase):

    def get_cribbage_schema_paths(self):
        cribbage_win_state_path = os.path.join(os.path.dirname(__file__), '../schemas/cribbage-win-state-schema.json')

        cribbage_valid_state_path = os.path.join(os.path.dirname(__file__),
                                                 '../schemas/cribbage-valid-state-schema.json')

        return cribbage_win_state_path, cribbage_valid_state_path


    def test_game_initial_game_state_valid(self):
        (cribbage_win_state_path, cribbage_valid_state_path) = self.get_cribbage_schema_paths()
        with open(cribbage_win_state_path) as win_state_file, open(cribbage_valid_state_path) as valid_state_file:
            win_state_schema = json.load(win_state_file)
            valid_state_schema = json.load(valid_state_file)
            gameRules = GameRules(
                key='key',
                winningSchema=win_state_schema,
                validStateSchema=valid_state_schema,
            )
            player_score_history_one = PlayerScoreHistory(
                key='one',
                scores=[],
                currentScore=2,
                playerKey='1',
                gameKey='1',
                order=0
            )
            player_score_history_two = PlayerScoreHistory(
                key='two',
                scores=[],
                currentScore=0,
                playerKey='2',
                gameKey='key',
                order=1
            )

            game = Game(
                key='key',
                description='Some description',
                date=1234,
                rules=gameRules,
                scoreHistory=[
                    player_score_history_one,
                    player_score_history_two,
                ]
            )

        assert validate_game_state(game) is True

    def test_invalid_game_state_valid(self):
        (cribbage_win_state_path, cribbage_valid_state_path) = self.get_cribbage_schema_paths()
        with open(cribbage_win_state_path) as win_state_file, open(cribbage_valid_state_path) as valid_state_file:
            win_state_schema = json.load(win_state_file)
            valid_state_schema = json.load(valid_state_file)
            gameRules = GameRules(
                key='key',
                winningSchema=win_state_schema,
                validStateSchema=valid_state_schema,
            )
            player_score_history_one = PlayerScoreHistory(
                key='one',
                scores=[],
                currentScore=2,
                playerKey='1',
                gameKey='1',
                order=0
            )

            game = Game(
                key='key',
                description='Some description',
                date=1234,
                rules=gameRules,
                scoreHistory=[
                    player_score_history_one,
                ]
            )

        self.assertRaises(ValidationError, validate_game_state, game)


    def test_game_initial_game_state_not_won(self):
        (cribbage_win_state_path, cribbage_valid_state_path) = self.get_cribbage_schema_paths()
        with open(cribbage_win_state_path) as win_state_file, open(cribbage_valid_state_path) as valid_state_file:
            win_state_schema = json.load(win_state_file)
            valid_state_schema = json.load(valid_state_file)
            gameRules = GameRules(
                key='key',
                winningSchema=win_state_schema,
                validStateSchema=valid_state_schema,
            )
            player_score_history_one = PlayerScoreHistory(
                key='one',
                scores=[],
                currentScore=0,
                playerKey='1',
                gameKey='1',
                order=0
            )
            player_score_history_two = PlayerScoreHistory(
                key='two',
                scores=[],
                currentScore=0,
                playerKey='2',
                gameKey='key',
                order=1
            )

            game = Game(
                key='key',
                description='Some description',
                date=1234,
                rules=gameRules,
                scoreHistory=[
                    player_score_history_one,
                    player_score_history_two,
                ]
            )

        assert is_game_won(game) is False

    def test_game_won(self):
        (cribbage_win_state_path, cribbage_valid_state_path) = self.get_cribbage_schema_paths()
        with open(cribbage_win_state_path) as win_state_file, open(cribbage_valid_state_path) as valid_state_file:
            win_state_schema = json.load(win_state_file)
            valid_state_schema = json.load(valid_state_file)
            gameRules = GameRules(
                key='key',
                winningSchema=win_state_schema,
                validStateSchema=valid_state_schema,
            )
            round_one = ScoreRound(scores=[121], roundScore=121, key='1', playerScoreHistoryKey='one', order=0)
            player_score_history_one = PlayerScoreHistory(
                key='one',
                scores=[round_one],
                currentScore=121,
                playerKey='1',
                gameKey='1',
                order=0
            )
            player_score_history_two = PlayerScoreHistory(
                key='two',
                scores=[],
                currentScore=0,
                playerKey='2',
                gameKey='key',
                order=1
            )

            game = Game(
                key='key',
                description='Some description',
                date=1234,
                rules=gameRules,
                scoreHistory=[
                    player_score_history_one,
                    player_score_history_two,
                ]
            )

        assert is_game_won(game) is True
