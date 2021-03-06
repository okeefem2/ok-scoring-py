from sqlalchemy import MetaData, Column, Table, Boolean, String
from sqlalchemy.dialects.postgresql import UUID

metadata = MetaData()

player = Table(
    "player",
    metadata,
    Column("key", UUID, primary_key=True),
    Column("name", String),
    Column("favorite", Boolean)
)

