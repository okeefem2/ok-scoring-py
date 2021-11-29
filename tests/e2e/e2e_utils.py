import json
import os
from typing import Optional

import requests
from dataclasses import dataclass
from ok_scoring.ok_scoring_config import get_api_url


@dataclass()
class PlayerScoreTestData:
    player_key: str
    score: int
    status: Optional[int] = 200


@dataclass()
class ScoreRoundTestData:
    scores: [PlayerScoreTestData]
    winning_player_key: str
    round_index: int


# Returns game key
def create_test_game(game: str, players: [str]) -> dict:
    base_schema_path = os.path.join(os.path.dirname(__file__), os.pardir, 'schemas')
    win_state_path = os.path.join(base_schema_path, f'{game}-win-state-schema.json')
    valid_state_path = os.path.join(base_schema_path, f'{game}-valid-state-schema.json')
    rules = {}
    with open(win_state_path) as win_state_file, open(valid_state_path) as valid_state_file:
        win_state_schema = json.load(win_state_file)
        valid_state_schema = json.load(valid_state_file)
        rules['winningSchema'] = win_state_schema
        rules['validStateSchema'] = valid_state_schema

    data = {
        'description': game,
        'players': players,
        'rules': rules
    }
    api_url = get_api_url()

    response = requests.post(f'{api_url}/games', json=data)
    assert response.status_code == 201
    game = response.json()['game']
    assert game['key'] is not None
    assert len(game['scoreHistory']) == len(players)

    return game


def play_test_game(rounds: [ScoreRoundTestData], game_key: str):
    api_url = get_api_url()
    for r in rounds:
        for s in r.scores:
            player_key = s.player_key
            data = {'round_index': r.round_index, 'score': s.score}
            update_score_response = requests.post(f'{api_url}/games/{game_key}/scores/{player_key}', json=data)
            assert update_score_response.status_code == s.status

            if s.status == 200:
                game = update_score_response.json()['game']
                scoreHistory = game['scoreHistory']
                player_score_history = next((sh for sh in scoreHistory if sh['playerKey'] == player_key), None)
                print(f'checking round {r.round_index} for {player_key}')
                assert player_score_history['scores'][r.round_index]['roundScore'] == s.score

        # Validate
        fetch_game_response = requests.get(f'{api_url}/games/{game_key}')
        game = fetch_game_response.json()['game']

        assert game['winningPlayerKey'] == r.winning_player_key