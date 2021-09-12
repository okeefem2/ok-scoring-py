import unittest
from ok_scoring.model.game import Game
from ok_scoring.service.game_rules_service_v2 import validate_game_state


class ValidateGameStateTest(unittest.TestCase):

    def test_game_with_no_rules_is_valid(self):
        game = Game(
            key='key',
            description='Some description',
            date=1234,
        )

        assert validate_game_state(game) is True
