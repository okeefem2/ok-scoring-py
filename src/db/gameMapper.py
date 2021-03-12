from sqlalchemy import MetaData, Column, Table, Integer, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID, ARRAY

metadata = MetaData()

player_score_history = Table(
    "game",
    metadata,
    Column("key", UUID, primary_key=True),
    Column("description", String),
    Column("date", Integer),
    Column("duration", Integer),
    Column("winningPlayerKey", UUID, ForeignKey("player.key"))
)
