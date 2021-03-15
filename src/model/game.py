from dataclasses import dataclass
from typing import Optional

from src.model.gameRules import GameRules
from src.model.playerScoreHistory import PlayerScoreHistory


@dataclass()
class Game:

    key: str
    description: str
    date: int

    duration: Optional[int] = None
    winningPlayerKey: Optional[str] = None

    # TODO this will need to be set after loading or something
    scoreHistory: dict[str, PlayerScoreHistory] = None
    scores: set[PlayerScoreHistory] = None
    rules: Optional[GameRules] = None
