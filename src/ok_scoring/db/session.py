from ok_scoring import ok_scoring_config
from ok_scoring.db import orm
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

orm.start_mappers()
engine = create_engine(ok_scoring_config.get_postgres_uri())
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
