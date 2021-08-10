from ok_scoring.model.player_score_history import PlayerScoreHistory
from ok_scoring.model.score_round import ScoreRound
from ok_scoring.model.validation_error import ValidationError
from ok_scoring.repository.helpers import unique_id
from ok_scoring.utils.list.fill_missing_indexes_to_length import fill_missing_indexes_to_length
from ok_scoring.utils.list.update_and_copy_list import update_and_copy_list


class PlayerKeyRequired(ValidationError):
    pass


class GameKeyRequired(ValidationError):
    pass


class OrderRequired(ValidationError):
    pass


def set_round_score(scoreHistory: PlayerScoreHistory, score, round_index, score_index):
    rounds = len(scoreHistory.scores)
    if round_index >= rounds:
        # default round score though...
        # if round_index is past the end of the current rounds list
        # round_index + 1 will be the new number of rounds
        # pad up to that round index with 0s
        # this code allows for idempotency, and the idea of eventual consistency if
        # round score updates come in out of order for some reason
        # Note filling the missing rounds does create a brand new list, so this will be picked up by sql alchemy
        # TODO pass in default round score
        round_scores = fill_missing_indexes_to_length(
            [],
            score_index + 1,
            lambda: 0
        )
        scoreHistory.scores = fill_missing_indexes_to_length(
            scoreHistory.scores,
            round_index + 1,
            lambda: ScoreRound(roundScore=0, scores=round_scores)
        )
    # have to replace the list to get sqlalchemy to pick up the update
    scoreRound = scoreHistory.scores[round_index]
    scoreRound.scores = fill_missing_indexes_to_length(scoreRound.scores, score_index, lambda: 0)
    scoreRound.scores = update_and_copy_list(scoreRound.scores, score, score_index)
    scoreRound = calculate_round_score(scoreRound)
    scoreHistory.scores = update_and_copy_list(scoreHistory.scores, scoreRound, round_index)
    scoreHistory.currentScore = calculate_current_score(scoreHistory.scores)
    return scoreHistory


def calculate_round_score(scoreRound: ScoreRound):
    if scoreRound is not None:
        scoreRound.roundScore = sum(scoreRound.scores)
    return scoreRound


def calculate_current_score(rounds: [ScoreRound]):
    return sum(score for scoreRound in rounds for score in scoreRound.scores) if rounds is not None else 0


def build_player_score_history(player_key: str, game_key: str, order: int, starting_score=0, scores=None) \
        -> PlayerScoreHistory:
    if player_key is None:
        raise PlayerKeyRequired(
            propertyPath=f'game.scoreHistory[{order}].playerKey',
            errorType='required',
            errorMessage='Player key required to create score history'
        )
    if game_key is None:
        raise GameKeyRequired(
            propertyPath=f'game.scoreHistory[{order}].gameKey',
            errorType='required',
            errorMessage='Game key required to create score history'
        )
    if order is None:
        raise OrderRequired(
            propertyPath=f'game.scoreHistory[{order}].order',
            errorType='required',
            errorMessage='Order required to create score history'
        )

    scores = scores if scores is not None else []

    return PlayerScoreHistory(
        key=unique_id(),
        gameKey=game_key,
        playerKey=player_key,
        currentScore=starting_score,
        scores=scores,
        order=order
    )


def build_score_history(player_keys, game_key: str, starting_score=0, scores=None) -> list[PlayerScoreHistory]:
    return [build_player_score_history(player_key=key, game_key=game_key, order=i, starting_score=starting_score, scores=scores) for i, key in enumerate(player_keys)]
    # If I ever use a dict for this structure again
    # return {key: build_player_score_history(key, game_key, starting_score, scores) for key in player_keys}


def find_by_player_key(scoreHistory: [PlayerScoreHistory], key: str) -> PlayerScoreHistory:
    return None if scoreHistory is None else next(
        filter(lambda playerScoreHistory: playerScoreHistory.playerKey == key, scoreHistory),
        None
    )


def find_by_order_index(scoreHistory: [PlayerScoreHistory], orderIndex) -> PlayerScoreHistory:
    return None if scoreHistory is None else next(
        filter(lambda playerScoreHistory: playerScoreHistory.order == orderIndex, scoreHistory),
        None
    )


def is_current_round(scoreHistory: [PlayerScoreHistory], round_index):
    score_history = max(scoreHistory, key=lambda s: len(s.scores) - 1)
    return len(score_history.scores) - 1 == round_index


# TODO this may be a rules service function
def is_round_complete(scoreHistory: [PlayerScoreHistory], round_index) -> bool:
    return scoreHistory is not None and len(scoreHistory) > 0 \
           and all(round_index < len(playerScoreHistory.scores) for playerScoreHistory in scoreHistory)

