from sqlalchemy import MetaData, Integer, Column, Table, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

metadata = MetaData()

gameRules = Table(
    "gameRules",
    metadata,
    Column("key", UUID, primary_key=True),
    Column("gameKey", UUID, ForeignKey("game.key")),
    Column("startingScore", Integer),
    Column("scoreIncreasesByDefault", Boolean),
    Column("defaultScoreStep", Integer),
    Column("rounds", Integer),
    Column("minRoundsToWin", Integer),
    Column("maxRounds", Integer),
    Column("minRoundScore", Integer),
    Column("maxRoundScore", Integer),
    Column("minPlayers", Integer),
    Column("maxPlayers", Integer),
    Column("winningScore", Integer),
    Column("canBust", Integer),
    Column("highScoreWins", Boolean),
)

