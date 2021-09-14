from dataclasses import dataclass


@dataclass()
class ScoreRound:
    key: str
    playerScoreHistoryKey: str
    scores: [int]
    roundScore: int
    order: int
