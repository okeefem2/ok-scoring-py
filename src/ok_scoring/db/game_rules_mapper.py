from sqlalchemy import Column, Table, Boolean, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID, JSONB

from ok_scoring.db.metadata import metadata

game_rules = Table(
    'gameRules',
    metadata,
    Column('key', UUID, primary_key=True),
    Column('gameKey', UUID, ForeignKey('game.key')),
    Column('validStateSchema', JSONB),
    Column('winningSchema', JSONB),
    Column('firstToScoreWins', Boolean),
    Column('scoreIncreasesByDefault', Boolean),
    Column('highScoreWins', Boolean),
    Column('playersMustBeOnSameRound', Boolean),
    Column('dealerSettings', String),
)

