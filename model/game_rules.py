from dataclasses import dataclass
from typing import Optional


# TODO think about how to make this more generic... think PROMISE rules
@dataclass(frozen=True)
class GameRules:
    key: str
    startingScore: Optional[int] = None
    defaultScoreStep: Optional[int] = None

    rounds: Optional[int] = None
    minRoundsToWin: Optional[int] = None
    maxRounds: Optional[int] = None

    minRoundScore: Optional[int] = None
    maxRoundScore: Optional[int] = None

    minPlayers: Optional[int] = None
    maxPlayers: Optional[int] = None

    winningScore: Optional[int] = None
    canBust: Optional[int] = None

    highScoreWins: Optional[bool] = None
    scoreIncreases: Optional[bool] = None

    # a Set of possible scores
    setScores: Optional[set[int]] = None
