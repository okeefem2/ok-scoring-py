from dataclasses import asdict

from src.model.gameRules import GameRules

rules = GameRules(key='one')
print(asdict(rules))
