from typing import Optional

from dataclasses import dataclass
from ok_scoring.model.player import Player


@dataclass()
class PlayerScoreHistory:
    currentScore: int
    scores: list[int]
    playerKey: str
    gameKey: str
    key: str
    order: int
    player: Optional[Player] = None
