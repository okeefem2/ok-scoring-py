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

    rules = {

    }
    description = 'Peanuts'
