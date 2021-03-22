from sqlalchemy import Column, Table, String
from sqlalchemy.dialects.postgresql import UUID

from ok_scoring.db.metadata import metadata

favorite_game = Table(
    'favoriteGames',
    metadata,
    Column('key', UUID, primary_key=True),
    Column('description', String)
)

