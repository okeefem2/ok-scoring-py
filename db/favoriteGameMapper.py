from sqlalchemy import MetaData, Column, Table, String
from sqlalchemy.dialects.postgresql import UUID

metadata = MetaData()

favoriteGame = Table(
    "favoriteGames",
    metadata,
    Column("key", UUID, primary_key=True),
    Column("description", String)
)

