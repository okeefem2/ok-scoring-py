from sqlalchemy import Column, Table, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ARRAY

from ok_scoring.db.metadata import metadata

player_score_history = Table(
    'playerScoreHistory',
    metadata,
    Column('key', UUID, primary_key=True),
    Column('scores', ARRAY(Integer)),
    Column('currentScore', Integer),
    Column('playerKey', UUID, ForeignKey('player.key')),
    Column('gameKey', UUID, ForeignKey('game.key'))
)
