from sqlalchemy import Column, Table, Boolean, String
from sqlalchemy.dialects.postgresql import UUID

from ok_scoring.db.metadata import metadata

player = Table(
    'player',
    metadata,
    Column('key', UUID, primary_key=True),
    Column('name', String),
    Column('favorite', Boolean)
)

