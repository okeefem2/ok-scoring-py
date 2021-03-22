import pytest
import requests



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

    assert response.status_code == 201
    game = response.json()
    assert game.key is not None

    # Next test fetching the game and checking equality to ensure persistence
