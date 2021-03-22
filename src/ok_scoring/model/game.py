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

    # TODO this will need to be set after loading or something
    scoreHistory: dict[str, PlayerScoreHistory] = None
    scores: set[PlayerScoreHistory] = None
    rules: Optional[GameRules] = None
