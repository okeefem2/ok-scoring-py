
from flask import Flask
from ok_scoring.db.session import db_session
from ok_scoring.entrypoints.games.routes import games


app = Flask(__name__)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/', methods=['GET'])
def home():
    return 'Hello OK Scoring', 201


app.register_blueprint(games, url_prefix='/games')
