from dataclasses import dataclass
from typing import Optional

from src.model.gameRules import GameRules
from src.model.playerScoreHistory import PlayerScoreHistory


@dataclass(frozen=True)
class Game:
    description: str
    date: int
    duration: int
    winningPlayerKey: str
    # TODO this will need to be set after loading or something
    scoreHistory: dict[str, PlayerScoreHistory]
    scores: set[PlayerScoreHistory]
    rules: Optional[GameRules] = None
