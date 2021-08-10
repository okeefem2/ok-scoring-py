from dataclasses import dataclass
from typing import Optional
from enum import Enum


class DealerSettings(Enum):
    Constant = 'constant'
    NewPerRound = 'newPerRound'
    Manual = 'manual'


@dataclass()
class GameRules:
    key: str
    gameKey: Optional[str] = None  # TODO think about this more
    # I wonder if it could be better to have rules be set in stone and create a join table
    # One big thing to think about will be editing rules though...
    # I think it would probably be better to have a rules template or something, and
    # Probably an optional foreign key on this table
    startingScore: Optional[int] = 0
    # Used to set default sign in the UI
    scoreIncreasesByDefault: Optional[bool] = True
    defaultScoreStep: Optional[int] = 0

    # TODO IDR what this one is haha
    rounds: Optional[int] = None
    minRoundsToWin: Optional[int] = None
    maxRounds: Optional[int] = None

    minRoundScore: Optional[int] = None
    maxRoundScore: Optional[int] = None

    minPlayers: Optional[int] = None
    maxPlayers: Optional[int] = None

    winningScore: Optional[int] = None
    firstToScoreWins: Optional[bool] = None
    canBust: Optional[int] = None

    highScoreWins: Optional[bool] = True

    # a Set of possible scores
    setScores: Optional[set[int]] = None

    dealerSettings: Optional[DealerSettings] = None

    # Determined how many scores can be in a round
    multipleScoresPerRound: Optional[bool] = None
    # Determines if all players must finish a round before moving on, or if it's a free for all
    playersMustBeOnSameRound: Optional[bool] = None

    # TODO add boolean to check for order of setScores

    # TODO a set of required score conditions - think yahtzee
    # TODO add rules for teams
