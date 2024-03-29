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

    response = requests.post(f'{api_url}/games', json=data)

    assert response.status_code == 201
    game = response.json()['game']
    assert game is not None
    game_key = game['key']
    assert game_key is not None
    assert game['rules'] is not None
    assert len(game['scoreHistory']) == 4

    # Next test fetching the game and checking equality to ensure persistence

    response = requests.get(f'{api_url}/games/{game_key}')

    assert response.status_code == 200
    game = response.json()['game']
    assert game is not None
    assert game['key'] is not None
    assert game['rules'] is not None
    assert len(game['scoreHistory']) == 4


@pytest.mark.usefixtures('restart_api')
def test_400_for_game_with_no_description():
    players = [
        'Meredith',
        'Maggie',
        'Amelia',
        'Lexie'
    ]
    rules = {
        'winningScore': 100
    }

    data = {
        'rules': rules,
        'players': players
    }

    api_url = get_api_url()

    response = requests.post(f'{api_url}/games', json=data)

    assert response.status_code == 400
    error = response.json()['error']
    assert error is not None
    assert error['path'] == 'game.description'


@pytest.mark.usefixtures('restart_api')
def test_players_not_duplicated_in_db():
    players = [
        'Meredith',
        'Maggie',
        'Amelia',
        'Lexie',
        'Meredith',
        'Maggie',
        'Amelia',
        'Lexie'
    ]

    data = {
        'description': 'Cribbage',
        'players': players
    }

    api_url = get_api_url()

    response = requests.post(f'{api_url}/games', json=data)
    assert response.status_code == 201
    game = response.json()['game']
    game_key = game['key']
    players_response = requests.get(f'{api_url}/games/{game_key}/players')
    assert players_response.status_code == 200
    players = players_response.json()['players']
    assert len(players) == 4
