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


@pytest.mark.usefixtures('restart_api')
def test_playing_cribbage():
    players = [
        'Geralt',
        'Ciri'
    ]

    rules = {
        'minPlayers': 2,
        'maxPlayers': 4,
        'winningScore': 121
    }

    data = {
        'description': 'Cribbage',
        'players': players,
        'rules': rules
    }

    api_url = get_api_url()

    response = requests.post(f'{api_url}/games', json=data)
    assert response.status_code == 201
    game = response.json()['game']
    game_key = game['key']
    players = response.json()['players']

    geralt_key = players[0]['key']
    ciri_key = players[1]['key']

    # TODO need to address the dealer and order of scoring parts of cribbage

    # TODO deletion
    scoreRounds = [
        # Geralt deals first
        {'scores': [{'playerKey': geralt_key, 'score': 11}, {'playerKey': ciri_key, 'score': 7}], 'winning': geralt_key, 'index': 0},
        {'scores': [{'playerKey': geralt_key, 'score': 5}, {'playerKey': ciri_key, 'score': 24}], 'winning': ciri_key, 'index': 1},
        {'scores': [{'playerKey': geralt_key, 'score': 15}, {'playerKey': ciri_key, 'score': 8}], 'winning': ciri_key, 'index': 2},  # G: 31, C: 39
        {'scores': [{'playerKey': geralt_key, 'score': 16}, {'playerKey': ciri_key, 'score': 6}], 'winning': geralt_key, 'index': 3},  # G: 47, C: 45
        {'scores': [{'playerKey': geralt_key, 'score': 0}, {'playerKey': ciri_key, 'score': 4}], 'winning': ciri_key, 'index': 4},  # G: 47, C: 49
        {'scores': [{'playerKey': geralt_key, 'score': 20}, {'playerKey': ciri_key, 'score': 14}], 'winning': geralt_key, 'index': 5},  # G: 67, C: 63
        {'scores': [{'playerKey': geralt_key, 'score': 10}, {'playerKey': ciri_key, 'score': 14}], 'winning': ciri_key, 'index': 5},  # Correction  G: 57, C: 63
        {'scores': [{'playerKey': geralt_key, 'score': 9}, {'playerKey': ciri_key, 'score': 12}], 'winning': ciri_key, 'index': 6},  # G: 66, C: 75
        {'scores': [{'playerKey': geralt_key, 'score': 8}, {'playerKey': ciri_key, 'score': 8}], 'winning': ciri_key, 'index': 7},  # G: 74, C: 83
        {'scores': [{'playerKey': geralt_key, 'score': 6}, {'playerKey': ciri_key, 'score': 8}], 'winning': ciri_key, 'index': 8},  # G: 82, C: 91
        {'scores': [{'playerKey': geralt_key, 'score': 16}, {'playerKey': ciri_key, 'score': 10}], 'winning': ciri_key, 'index': 9},  # G: 96, C: 101
        {'scores': [{'playerKey': geralt_key, 'score': 4}, {'playerKey': ciri_key, 'score': 12}], 'winning': ciri_key, 'index': 10},  # G: 100, C: 113
        # Geralt actually wins because he scores first, currently not working though
        {'scores': [{'playerKey': geralt_key, 'score': 24}, {'playerKey': ciri_key, 'score': 14, 'status': 422}], 'winning': geralt_key, 'index': 11},  # G: 124, C: 127
    ]

    for scoreRound in scoreRounds:
        for score in scoreRound['scores']:
            player_key = score['playerKey']
            data = {'score_index': scoreRound['index'], 'score': score['score']}
            status = 200 if 'status' not in score else score['status']
            update_score_response = requests.post(f'{api_url}/games/{game_key}/scores/{player_key}', json=data)
            assert update_score_response.status_code == status

            if status == 200:
                game = update_score_response.json()['game']
                scoreHistory = game['scoreHistory']
                player_score_history = next((s for s in scoreHistory if s['playerKey'] == player_key), None)
                assert player_score_history['scores'][scoreRound['index']] == score['score']

        # Validate
        fetch_game_response = requests.get(f'{api_url}/games/{game_key}', json=data)
        game = fetch_game_response.json()['game']

        assert game['winningPlayerKey'] == scoreRound['winning']




