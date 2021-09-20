import pytest
import requests
from ok_scoring.ok_scoring_config import get_api_url


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

    scoreRounds = [
        # Geralt deals first
        {'scores': [{'playerKey': geralt_key, 'score': 11}, {'playerKey': ciri_key, 'score': 7}], 'winning': geralt_key, 'round_index': 0},
        {'scores': [{'playerKey': geralt_key, 'score': 5}, {'playerKey': ciri_key, 'score': 24}], 'winning': ciri_key, 'round_index': 1},
        {'scores': [{'playerKey': geralt_key, 'score': 15}, {'playerKey': ciri_key, 'score': 8}], 'winning': ciri_key, 'round_index': 2},  # G: 31, C: 39
        {'scores': [{'playerKey': geralt_key, 'score': 16}, {'playerKey': ciri_key, 'score': 6}], 'winning': geralt_key, 'round_index': 3},  # G: 47, C: 45
        {'scores': [{'playerKey': geralt_key, 'score': 0}, {'playerKey': ciri_key, 'score': 4}], 'winning': ciri_key, 'round_index': 4},  # G: 47, C: 49
        {'scores': [{'playerKey': geralt_key, 'score': 20}, {'playerKey': ciri_key, 'score': 14}], 'winning': geralt_key, 'round_index': 5},  # G: 67, C: 63
        {'scores': [{'playerKey': geralt_key, 'score': 10}, {'playerKey': ciri_key, 'score': 14}], 'winning': ciri_key, 'round_index': 5},  # Correction  G: 57, C: 63
        {'scores': [{'playerKey': geralt_key, 'score': 9}, {'playerKey': ciri_key, 'score': 12}], 'winning': ciri_key, 'round_index': 6},  # G: 66, C: 75
        {'scores': [{'playerKey': geralt_key, 'score': 8}, {'playerKey': ciri_key, 'score': 8}], 'winning': ciri_key, 'round_index': 7},  # G: 74, C: 83
        {'scores': [{'playerKey': geralt_key, 'score': 6}, {'playerKey': ciri_key, 'score': 8}], 'winning': ciri_key, 'round_index': 8},  # G: 82, C: 91
        {'scores': [{'playerKey': geralt_key, 'score': 16}, {'playerKey': ciri_key, 'score': 10}], 'winning': ciri_key, 'round_index': 9},  # G: 96, C: 101
        {'scores': [{'playerKey': geralt_key, 'score': 4}, {'playerKey': ciri_key, 'score': 12}], 'winning': ciri_key, 'round_index': 10},  # G: 100, C: 113
        # Geralt actually wins because he scores first, so ciri should get a 422 because the game is over at that point
        {'scores': [{'playerKey': geralt_key, 'score': 24}, {'playerKey': ciri_key, 'score': 14, 'status': 422}], 'winning': geralt_key, 'round_index': 11},  # G: 124, C: 127
    ]

    for scoreRound in scoreRounds:
        for score in scoreRound['scores']:
            round_index = scoreRound['round_index']
            player_key = score['playerKey']
            data = {'round_index': round_index, 'score': score['score']}
            status = 200 if 'status' not in score else score['status']
            update_score_response = requests.post(f'{api_url}/games/{game_key}/scores/{player_key}', json=data)
            assert update_score_response.status_code == status

            if status == 200:
                game = update_score_response.json()['game']
                scoreHistory = game['scoreHistory']
                player_score_history = next((s for s in scoreHistory if s['playerKey'] == player_key), None)
                print(f'checking round {round_index} for {player_key}')
                assert player_score_history['scores'][round_index]['roundScore'] == score['score']

        # Validate
        fetch_game_response = requests.get(f'{api_url}/games/{game_key}', json=data)
        game = fetch_game_response.json()['game']

        assert game['winningPlayerKey'] == scoreRound['winning']
