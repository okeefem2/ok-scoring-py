from sqlalchemy import Column, Table, Integer, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID, BIGINT

from ok_scoring.db.metadata import metadata

game = Table(
    'game',
    metadata,
    Column('key', UUID, primary_key=True),
    Column('description', String),
    Column('date', BIGINT),
    Column('duration', Integer),
    Column('winningPlayerKey', UUID, ForeignKey('player.key'))
)
