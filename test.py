from dataclasses import asdict

from ok_scoring.model.game_rules import GameRules

rules = GameRules(key='one')
print(asdict(rules))
