import pytest
import requests
from ok_scoring.ok_scoring_config import get_api_url


@pytest.mark.usefixtures('restart_api')
def test_api_returns_game():
    players = [
        'Meredith',
        'Maggie',
        'Amelia',
        'Lexie'
    ]
    rules = {
        'winningScore': 100
    }
    description = 'Peanuts'

    data = {
        'description': description,
        'rules': rules,
        'players': players
    }

    api_url = get_api_url()

    response = requests.post(f'{api_url}/game', json=data)
    print('response!', response.json())

    assert response.status_code == 201
    game = response.json()['game']
    assert game is not None
    assert game['key'] is not None

    # Next test fetching the game and checking equality to ensure persistence
