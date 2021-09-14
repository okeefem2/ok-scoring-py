from sqlalchemy import Integer, Column, Table, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ARRAY

from ok_scoring.db.metadata import metadata

score_round = Table(
    'scoreRound',
    metadata,
    Column('key', UUID, primary_key=True),
    Column('playerScoreHistoryKey', UUID, ForeignKey('playerScoreHistory.key')),
    Column('scores', ARRAY(Integer)),
    Column('roundScore', Integer, nullable=False),
    Column('order', Integer, nullable=False),
)

