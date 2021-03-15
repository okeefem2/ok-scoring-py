import time

from src.model.game import Game
from src.model.gameRules import GameRules
from src.repository.helpers import unique_id
from src.service.game_rules_service import validate_rounds, validate_score, validate_players

# Create a builder function
from src.service.player_score_history_service import set_round_score, build_score_history


class DescriptionRequired(Exception):
    pass


def add_player_round(game, playerKey: str, score: int, round_index: int):
    if can_add_player_round(game, playerKey, score):
        set_round_score(game.scoreHistory[playerKey], score, round_index)


def can_add_player_round(game, playerKey: str, score: int) -> bool:
    # Maybe could have a rule to add the player if they do not exist
    if playerKey not in game.scoreHistory:
        return False
    if game.rules is None:  # NO RULES!!
        return True

    playerScoreHistory = game.scoreHistory[playerKey]
    return validate_rounds(game.rules, len(playerScoreHistory.scores)) \
           and validate_score(game.rules, playerScoreHistory.currentScore, score)


def create_game(description, players=None, rules: GameRules = None) -> Game:
    if validate_players(rules, players):
        if description is None:
            raise DescriptionRequired('Description required to create game')

        game_key = unique_id()
        date = int(time.time() * 1000)
        game = Game(
            key=game_key,
            date=date,
            description=description,
            rules=rules
        )

        game.scoreHistory = build_score_history(
            players,
            game_key,
            rules.startingScore if rules is not None else 0
        )
        game.scores = set()
        return game
