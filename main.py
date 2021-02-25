from dataclasses import dataclass
from typing import Optional

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

    def add_round(self, score):
        self.scores.append(score)
        self.currentScore += score

# TODO think about how to make this more generic... think PROMISE rules
@dataclass(frozen=True)
class GameRules:
    key: str
    startingScore: Optional[int] = None
    defaultScoreStep: Optional[int] = None

    rounds: Optional[int] = None
    minRoundsToWin: Optional[int] = None
    maxRounds: Optional[int] = None

    highScoreWins: Optional[bool] = None
    scoreIncreases: Optional[bool] = None

    minPlayers: Optional[int] = None
    maxPlayers: Optional[int] = None

    winningScore: Optional[int] = None
    canBust: Optional[int] = None


class ExceededRounds(Exception):
    pass


class Game:
    scoreHistory: dict[str, PlayerScoreHistory]
    rules: GameRules

    def __init__(self, scoreHistory, rules=None):
        self.scoreHistory = scoreHistory
        self.rules = rules

    # TODO move validation logic to "service functions"

    # Rules specific functions, may want to move these somewhere else...
    def validate_rounds(self, rounds):
        if self.rules.rounds is not None and rounds + 1 > self.rules.rounds:
            raise ExceededRounds(f'Max number of rounds already met {self.rules.rounds}')
        return True

    def validate_score(self, current_score, score):
        if self.rules.canBust and self.rules.highScoreWins and current_score + score > self.rules.winningScore:
            return False
        if self.rules.canBust and not self.rules.highScoreWins and current_score + score < self.rules.winningScore:
            return False
        return True
    ####################################################################################################################

    def can_add_player_round(self, playerKey: str, score: int):
        # Maybe could have a rule to add the player if they do not exist
        if playerKey not in self.scoreHistory:
            return False
        if self.rules is None:  # NO RULES!!
            return True

        playerScoreHistory = self.scoreHistory[playerKey]
        return self.validate_rounds(len(playerScoreHistory.scores)) and \
               self.validate_score(playerScoreHistory.currentScore, score)

    def add_player_round(self, playerKey: str, score: int):
        if self.can_add_player_round(playerKey, score):
            self.scoreHistory[playerKey].add_round(score)


def test_adding_round_score_updates_current_score():
    player_score_history_one = PlayerScoreHistory(key='one', scores=[1, 3, -2], currentScore=1)
    player_score_history_one.add_round(6)
    assert player_score_history_one.currentScore == 7

    player_score_history_one.add_round(-10)
    assert player_score_history_one.currentScore == -3


def test_cannot_add_score_for_non_player_no_rules():
    player_score_history_one = PlayerScoreHistory(key='one', scores=[1, 3, -2], currentScore=1)
    game = Game(scoreHistory={'one': player_score_history_one})
    assert game.can_add_player_round('two', 6) is False

def test_can_add_score_for_player_no_rules():
    player_score_history_one = PlayerScoreHistory(key='one', scores=[1, 3, -2], currentScore=1)
    game = Game(scoreHistory={'one': player_score_history_one})
    assert game.can_add_player_round('one', 6) is True

def test_can_add_score_for_player_under_round_cap():
    player_score_history_one = PlayerScoreHistory(key='one', scores=[1, 3, -2], currentScore=1)
    rules = GameRules(key="rules_one", rounds=5)
    game = Game(scoreHistory={'one': player_score_history_one}, rules=rules)
    assert game.can_add_player_round('one', 6) is True

def test_can_add_score_for_player_meeting_round_cap():
    player_score_history_one = PlayerScoreHistory(key='one', scores=[1, 3, -2], currentScore=1)
    rules = GameRules(key="rules_one", rounds=4)
    game = Game(scoreHistory={'one': player_score_history_one}, rules=rules)
    assert game.can_add_player_round('one', 6) is True

def test_cannot_add_score_for_player_at_round_cap():
    player_score_history_one = PlayerScoreHistory(key='one', scores=[1, 3, -2], currentScore=1)
    rules = GameRules(key="rules_one", rounds=3)
    game = Game(scoreHistory={'one': player_score_history_one}, rules=rules)
    assert game.can_add_player_round('one', 6) is False

def test_cannot_add_score_for_player_that_busts_positive():
    player_score_history_one = PlayerScoreHistory(key='one', scores=[1, 3, -2], currentScore=1)
    rules = GameRules(key="rules_one", canBust=True, winningScore=5, highScoreWins=True)
    game = Game(scoreHistory={'one': player_score_history_one}, rules=rules)
    assert game.can_add_player_round('one', 6) is False

def test_cannot_add_score_for_player_that_busts_negative():
    player_score_history_one = PlayerScoreHistory(key='one', scores=[1, 3, -2], currentScore=1)
    rules = GameRules(key="rules_one", canBust=True, winningScore=0, highScoreWins=False)
    game = Game(scoreHistory={'one': player_score_history_one}, rules=rules)
    assert game.can_add_player_round('one', -6) is False

if __name__ == '__main__':
    test_adding_round_score_updates_current_score()
    test_cannot_add_score_for_non_player_no_rules()
    test_can_add_score_for_player_no_rules()
    test_can_add_score_for_player_under_round_cap()
    test_can_add_score_for_player_meeting_round_cap()
    test_cannot_add_score_for_player_at_round_cap()
    test_cannot_add_score_for_player_that_busts_positive()
    test_cannot_add_score_for_player_that_busts_negative()

