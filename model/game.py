from dataclasses import dataclass
from typing import Optional

from model.game_rules import GameRules
from model.player_score_history import PlayerScoreHistory


@dataclass(frozen=True)
class Game:
    scoreHistory: dict[str, PlayerScoreHistory]
    rules: Optional[GameRules] = None
