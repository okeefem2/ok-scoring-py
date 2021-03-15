from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import ok_scoring_config
from src.db import orm

if __name__ == '__main__':
    orm.startMappers()
    get_session = sessionmaker(bind=create_engine(ok_scoring_config.get_postgres_uri()))
    app = Flask(__name__)
