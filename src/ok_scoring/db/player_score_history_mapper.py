from ok_scoring.model.score_round import ScoreRound
from sqlalchemy import Column, Table, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB

from ok_scoring.db.metadata import metadata

player_score_history = Table(
    'playerScoreHistory',
    metadata,
    Column('key', UUID, primary_key=True),
    Column('currentScore', Integer, nullable=False),
    Column('order', Integer),
    Column('playerKey', UUID, ForeignKey('player.key')),
    Column('gameKey', UUID, ForeignKey('game.key'))
)
