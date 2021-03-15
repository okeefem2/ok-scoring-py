from sqlalchemy import Column, Table, String
from sqlalchemy.dialects.postgresql import UUID

from src.db.orm import metadata

favorite_game = Table(
    "favoriteGames",
    metadata,
    Column("key", UUID, primary_key=True),
    Column("description", String)
)

