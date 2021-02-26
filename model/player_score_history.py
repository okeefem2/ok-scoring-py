from dataclasses import dataclass


@dataclass()
class PlayerScoreHistory:
    key: str
    currentScore: int
    scores: list[int]
