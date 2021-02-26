from sqlalchemy import MetaData, Integer, Column, Table, Boolean
from sqlalchemy.dialects.postgresql import UUID

metadata = MetaData()

game_rules = Table(
    "game_rules",
    metadata,
    Column("key", UUID, primary_key=True),
    Column("startingScore", Integer),
    Column("defaultScoreStep", Integer),
    Column("rounds", Integer),
    Column("minRoundsToWin", Integer),
    Column("maxRounds", Integer),
    Column("minPlayers", Integer),
    Column("maxPlayers", Integer),
    Column("winningScore", Integer),
    Column("canBust", Integer),
    Column("highScoreWins", Boolean),
    Column("scoreIncreases", Boolean),
)

