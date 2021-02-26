class PlayerScoreHistory:
    key: str
    scores: list[int]
    currentScore: int

    def __init__(
            self, key: str, scores=None, currentScore=0
    ):
        self.key = key
        self.scores = [] if scores is None else scores
        self.currentScore = currentScore

    def set_round_score(self, score, round_index):
        rounds = len(self.scores)
        if round_index >= rounds:
            # default round score though...
            # if round_index is past the end of the current rounds list
            # round_index + 1 will be the new number of rounds
            # pad up to that round index with 0s
            # this code allows for idempotency, and the idea of eventual consistency if
            # round score updates come in out of order for some reason
            self.scores = self.scores + [0] * (round_index + 1 - rounds)
        self.scores[round_index] = score
        self.calculate_current_score()

    def calculate_current_score(self):
        self.currentScore = sum(self.scores)
