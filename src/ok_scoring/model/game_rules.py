from dataclasses import dataclass
from typing import Optional

from ok_scoring.model.dealer_settings import DealerSettings


@dataclass()
class GameRules:
    key: str
    gameKey: Optional[str] = None  # TODO think about this more
    # I wonder if it could be better to have rules be set in stone and create a join table
    # One big thing to think about will be editing rules though...
    # I think it would probably be better to have a rules template or something, and
    # Probably an optional foreign key on this table
    # Used to set default sign in the UI

    # TODO IDR what this one is haha
    rounds: Optional[int] = None

    # can be done in json schema
    startingScore: Optional[int] = 0
    minRoundsToWin: Optional[int] = None
    maxRounds: Optional[int] = None
    minRoundScore: Optional[int] = None
    maxRoundScore: Optional[int] = None
    minPlayers: Optional[int] = None
    maxPlayers: Optional[int] = None
    winningScore: Optional[int] = None
    canBust: Optional[int] = None
    setScores: Optional[set[int]] = None
    multipleScoresPerRound: Optional[bool] = None
    defaultScoreStep: Optional[int] = 0

    # cannot be done in json schema
    scoreIncreasesByDefault: Optional[bool] = True
    firstToScoreWins: Optional[bool] = None
    highScoreWins: Optional[bool] = True
    dealerSettings: Optional[DealerSettings] = None
    # Determines if all players must finish a round before moving on, or if it's a free for all
    playersMustBeOnSameRound: Optional[bool] = None

    # TODO add boolean to check for order of setScores
    # TODO a set of required score conditions - think yahtzee
    # TODO add rules for teams
