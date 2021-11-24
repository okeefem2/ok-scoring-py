from dataclasses import dataclass
from typing import Optional

from ok_scoring.model.dealer_settings import DealerSettings


@dataclass()
class GameRules:
    key: str
    validStateSchema: dict = None
    winningSchema: dict = None
    gameKey: Optional[str] = None

    # cannot be done in json schema... should these be a separate table?
    scoreIncreasesByDefault: Optional[bool] = True
    # Determines if we are done scoring as soon as the goal score is met, really only valuable with a winning score
    # And really would only not be true if you were allowed a "rebuttal"
    firstToScoreWins: Optional[bool] = None
    highScoreWins: Optional[bool] = True
    dealerSettings: Optional[DealerSettings] = None
    # Determines if all players must finish a round before moving on, or if it's a free for all
    playersMustBeOnSameRound: Optional[bool] = None
