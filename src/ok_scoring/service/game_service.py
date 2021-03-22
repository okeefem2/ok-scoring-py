import time

from ok_scoring.model.game import Game
from ok_scoring.model.game_rules import GameRules
from ok_scoring.model.player import Player
from ok_scoring.repository.helpers import unique_id

# Create a builder function
from ok_scoring.service.game_rules_service import validate_rounds, validate_score, validate_players
from ok_scoring.service.player_score_history_service import set_round_score, build_score_history


class DescriptionRequired(Exception):
    pass


def add_player_round(game, playerKey: str, score: int, round_index: int):
    if can_add_player_round(game.scoreHistory, game.rules, playerKey, score):
        set_round_score(game.scoreHistory[playerKey], score, round_index)


def can_add_player_round(scoreHistory, rules, playerKey: str, score: int) -> bool:
    # Maybe could have a rule to add the player if they do not exist
    if playerKey not in scoreHistory:
        return False
    if rules is None:  # NO RULES!!
        return True

    playerScoreHistory = scoreHistory[playerKey]
    return validate_rounds(rules, len(playerScoreHistory.scores)) \
           and validate_score(rules, playerScoreHistory.currentScore, score)


def create_game(description, players: [Player] = None, rules: GameRules = None) -> Game:
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
