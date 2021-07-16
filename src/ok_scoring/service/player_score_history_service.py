from ok_scoring.model.player_score_history import PlayerScoreHistory
from ok_scoring.repository.helpers import unique_id


def set_round_score(scoreHistory: PlayerScoreHistory, score, round_index):
    rounds = len(scoreHistory.scores)
    if round_index >= rounds:
        # default round score though...
        # if round_index is past the end of the current rounds list
        # round_index + 1 will be the new number of rounds
        # pad up to that round index with 0s
        # this code allows for idempotency, and the idea of eventual consistency if
        # round score updates come in out of order for some reason
        # Note filling the missing rounds does create a brand new list, so this will be picked up by sql alchemy
        scoreHistory.scores = fill_missing_rounds(scoreHistory.scores, round_index + 1, rounds)
    # have to replace the list to get sqlalchemy to pick up the update
    scoreHistory.scores = [score if i == round_index else s for i, s in enumerate(scoreHistory.scores)]
    scoreHistory.currentScore = calculate_current_score(scoreHistory.scores)
    return scoreHistory


def fill_missing_rounds(scores, ending_rounds, current_rounds):
    return scores + [0] * (ending_rounds - current_rounds)


def calculate_current_score(scores):
    return sum(scores)


def build_player_score_history(player_key, game_key, order, starting_score=0, scores=None, ) -> PlayerScoreHistory:
    scores = scores if scores is not None else []

    return PlayerScoreHistory(
        key=unique_id(),
        gameKey=game_key,
        playerKey=player_key,
        currentScore=starting_score,
        scores=scores,
        order=order
    )


def build_score_history(player_keys, game_key, starting_score=0, scores=None) -> list[PlayerScoreHistory]:
    return [build_player_score_history(player_key=key, game_key=game_key, order=i, starting_score=starting_score, scores=scores) for i, key in enumerate(player_keys)]
    # If I ever use a dict for this structure again
    # return {key: build_player_score_history(key, game_key, starting_score, scores) for key in player_keys}
