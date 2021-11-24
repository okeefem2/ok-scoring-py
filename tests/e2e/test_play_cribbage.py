import pytest

from tests.e2e.e2e_utils import create_test_game, ScoreRoundTestData, PlayerScoreTestData, play_test_game


@pytest.mark.usefixtures('restart_api')
def test_playing_cribbage():
    players = [
        'Geralt',
        'Ciri'
    ]

    game = create_test_game('cribbage', players)

    geralt_key = game['scoreHistory'][0]['playerKey']
    ciri_key = game['scoreHistory'][1]['playerKey']

    rounds: [ScoreRoundTestData] = [
        # Geralt deals first
        ScoreRoundTestData(
            scores=[PlayerScoreTestData(player_key=geralt_key, score=11), PlayerScoreTestData(player_key=ciri_key, score=7)],
            winning_player_key=geralt_key,
            round_index=0,
        ),  # G: 11, C: 7
        ScoreRoundTestData(
            scores=[PlayerScoreTestData(player_key=geralt_key, score=5), PlayerScoreTestData(player_key=ciri_key, score=24)],
            winning_player_key=ciri_key,
            round_index=1,
        ),  # G: 16, C: 31
        ScoreRoundTestData(
            scores=[PlayerScoreTestData(player_key=geralt_key, score=15), PlayerScoreTestData(player_key=ciri_key, score=8)],
            winning_player_key=ciri_key,
            round_index=2,
        ),  # G: 31, C: 39
        ScoreRoundTestData(
            scores=[PlayerScoreTestData(player_key=geralt_key, score=16), PlayerScoreTestData(player_key=ciri_key, score=6)],
            winning_player_key=geralt_key,
            round_index=3,
        ),  # G: 47, C: 45
        ScoreRoundTestData(
            scores=[PlayerScoreTestData(player_key=geralt_key, score=0), PlayerScoreTestData(player_key=ciri_key, score=4)],
            winning_player_key=ciri_key,
            round_index=4,
        ),  # G: 47, C: 49
        ScoreRoundTestData(
            scores=[PlayerScoreTestData(player_key=geralt_key, score=20), PlayerScoreTestData(player_key=ciri_key, score=14)],
            winning_player_key=geralt_key,
            round_index=5,
        ),  # G: 67, C: 63
        ScoreRoundTestData(
            scores=[PlayerScoreTestData(player_key=geralt_key, score=10), PlayerScoreTestData(player_key=ciri_key, score=14)],
            winning_player_key=ciri_key,
            round_index=5,
        ),  # Correction  G: 57, C: 63
        ScoreRoundTestData(
            scores=[PlayerScoreTestData(player_key=geralt_key, score=9), PlayerScoreTestData(player_key=ciri_key, score=12)],
            winning_player_key=ciri_key,
            round_index=6,
        ),  # G: 66, C: 75
        ScoreRoundTestData(
            scores=[PlayerScoreTestData(player_key=geralt_key, score=8), PlayerScoreTestData(player_key=ciri_key, score=7)],
            winning_player_key=ciri_key,
            round_index=7,
        ),  # G: 74, C: 83
        ScoreRoundTestData(
            scores=[PlayerScoreTestData(player_key=geralt_key, score=6), PlayerScoreTestData(player_key=ciri_key, score=8)],
            winning_player_key=ciri_key,
            round_index=8,
        ),  # G: 82, C: 91
        ScoreRoundTestData(
            scores=[PlayerScoreTestData(player_key=geralt_key, score=16), PlayerScoreTestData(player_key=ciri_key, score=10)],
            winning_player_key=ciri_key,
            round_index=9,
        ),  # G: 96, C: 101
        ScoreRoundTestData(
            scores=[PlayerScoreTestData(player_key=geralt_key, score=4), PlayerScoreTestData(player_key=ciri_key, score=12)],
            winning_player_key=ciri_key,
            round_index=10,
        ),  # G: 100, C: 113
        # Geralt actually wins because he scores first, so ciri should get a 422 because the game is over at that point
        ScoreRoundTestData(
            scores=[PlayerScoreTestData(player_key=geralt_key, score=24), PlayerScoreTestData(player_key=ciri_key, score=14, status=422)],
            winning_player_key=geralt_key,
            round_index=11,
        ),  # G: 124, C: 113
    ]

    game_key = game['key']

    play_test_game(rounds, game_key)
