from sqlalchemy.orm import mapper

from db.game_rules_mapper import game_rules
from model.game_rules import GameRules


def start_mappers():
    game_rules_mapper = mapper(GameRules, game_rules)