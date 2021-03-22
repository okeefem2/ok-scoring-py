from dataclasses import dataclass


@dataclass()
class PlayerScoreHistory:
    currentScore: int
    scores: list[int]
    playerKey: str
    gameKey: str
    key: str = None
