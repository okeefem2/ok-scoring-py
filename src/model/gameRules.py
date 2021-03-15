from dataclasses import dataclass
from typing import Optional


@dataclass()
class GameRules:
    key: str
    gameKey: Optional[str] = None  # TODO think about this more
    # I wonder if it could be better to have rules be set in stone and create a join table
    # One big thing to think about will be editing rules though...
    # I think it would probably be better to have a rules template or something, and
    # Probably an optional foreign key on this table
    startingScore: Optional[int] = None
    # Used to set default sign in the UI
    scoreIncreasesByDefault: Optional[bool] = None
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

    # a Set of possible scores
    setScores: Optional[set[int]] = None

    # TODO a set of required score conditions - think yahtzee
