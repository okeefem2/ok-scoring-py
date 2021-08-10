from typing import Optional

from dataclasses import dataclass
from ok_scoring.model.player import Player
from ok_scoring.model.score_round import ScoreRound


@dataclass()
class PlayerScoreHistory:
    currentScore: int
    scores: list[ScoreRound]
    playerKey: str
    gameKey: str
    key: str
    order: int
    player: Optional[Player] = None
