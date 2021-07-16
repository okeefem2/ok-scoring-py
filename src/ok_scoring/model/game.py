from dataclasses import dataclass
from typing import Optional

from ok_scoring.model.game_rules import GameRules
from ok_scoring.model.player_score_history import PlayerScoreHistory


@dataclass()
class Game:

    key: str
    description: str
    date: int

    duration: Optional[int] = None
    winningPlayerKey: Optional[str] = None
    activePlayerKey: Optional[str] = None
    dealingPlayerKey: Optional[str] = None

    scoreHistory: Optional[list[PlayerScoreHistory]] = None
    rules: Optional[GameRules] = None
