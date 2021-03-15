from sqlalchemy import Column, Table, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ARRAY

from src.db.orm import metadata

player_score_history = Table(
    "playerScoreHistory",
    metadata,
    Column("key", UUID, primary_key=True),
    Column("scores", ARRAY),
    Column("currentScore", Integer),
    Column("playerKey", UUID, ForeignKey("player.key")),
    Column("gameKey", UUID, ForeignKey("game.key"))
)
