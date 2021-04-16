"""Update date column to BIGINT

Revision ID: 6b96d80d8d23
Revises: b0746df0549f
Create Date: 2021-04-15 23:45:38.777966

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '6b96d80d8d23'
down_revision = 'b0746df0549f'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        table_name='game',
        column_name='date',
        type_=postgresql.BIGINT
    )


def downgrade():
    op.alter_column(
        table_name='game',
        column_name='date',
        type_=sa.Integer
    )
