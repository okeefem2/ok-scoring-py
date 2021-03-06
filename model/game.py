from dataclasses import dataclass
from typing import Optional

from model.gameRules import GameRules
from model.playerScoreHistory import PlayerScoreHistory


@dataclass(frozen=True)
class Game:
    description: str
    date: int
    duration: int
    winningPlayerKey: str
    # TODO how do these work with the mapper
    scoreHistory: dict[str, PlayerScoreHistory]
    rules: Optional[GameRules] = None
