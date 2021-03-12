from src.model.playerScoreHistory import PlayerScoreHistory


def set_round_score(scoreHistory: PlayerScoreHistory, score, round_index):
    rounds = len(scoreHistory.scores)
    if round_index >= rounds:
        # default round score though...
        # if round_index is past the end of the current rounds list
        # round_index + 1 will be the new number of rounds
        # pad up to that round index with 0s
        # this code allows for idempotency, and the idea of eventual consistency if
        # round score updates come in out of order for some reason
        scoreHistory.scores = fill_missing_rounds(scoreHistory.scores, round_index + 1, rounds)
    scoreHistory.scores[round_index] = score
    scoreHistory.currentScore = calculate_current_score(scoreHistory.scores)


def fill_missing_rounds(scores, ending_rounds, current_rounds):
    return scores + [0] * (ending_rounds - current_rounds)


def calculate_current_score(scores):
    return sum(scores)
