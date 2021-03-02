from dataclasses import dataclass


@dataclass()
class PlayerScoreHistory:
    currentScore: int
    scores: list[int]
    key: str = None
