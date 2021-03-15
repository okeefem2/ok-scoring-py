import pytest

from src.model.game import Game
from src.model.gameRules import GameRules
from src.repository.helpers import unique_id, now


@pytest.mark.usefixtures('restart_api')
def test_api_returns_game(add_game):
    players = [
        'Meredith',
        'Maggie',
        'Amelia',
        'Lexie'
    ]

    game_key = unique_id()
    date = now()

    # game = create_game()

    rules = GameRules(key=unique_id(), winningScore=100, gameKey=game_key)
