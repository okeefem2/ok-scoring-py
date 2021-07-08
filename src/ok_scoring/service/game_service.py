import time

from ok_scoring.model.game import Game
from ok_scoring.model.game_rules import GameRules
from ok_scoring.model.player import Player
from ok_scoring.model.player_score_history import PlayerScoreHistory
from ok_scoring.model.validation_error import ValidationError
from ok_scoring.repository.abstract_repository import AbstractRepository
from ok_scoring.repository.helpers import unique_id, now

# Create a builder function
from ok_scoring.service.game_rules_service import validate_rounds, validate_score, validate_players, determine_winner
from ok_scoring.service.player_score_history_service import set_round_score, build_score_history


class DescriptionRequired(ValidationError):
    pass


def update_winner(game):
    game.winningPlayerKey = determine_winner(scoreHistory=game.scoreHistory, rules=game.rules)
    return game


def validate_and_set_round_score(scoreHistory: PlayerScoreHistory, rules: GameRules, score: int, round_index: int):
    if can_add_player_round(scoreHistory=scoreHistory, rules=rules, score=score):
        scoreHistory = set_round_score(scoreHistory, score, round_index)
    return scoreHistory


def can_add_player_round(scoreHistory: PlayerScoreHistory, rules, score: int) -> bool:
    if rules is None:  # NO RULES!!
        return True

    return validate_rounds(rules, len(scoreHistory.scores)) \
           and validate_score(rules, scoreHistory.currentScore, score)


def create_game(repo: AbstractRepository, description, players: [Player] = None, rules: GameRules = None) -> Game:
    game = build_new_game(description=description, players=players, rules=rules)
    # Save game to DB
    repo.add(game)

    return game


def build_new_game(description: str, players: [Player] = None, rules: GameRules = None) -> Game:
    if validate_players(rules=rules, players=players):
        if description is None:
            raise DescriptionRequired(
                propertyPath='game.description',
                errorType='required',
                errorMessage='Description required to create game')

        game_key = unique_id()
        date = now()

        score_history = build_score_history(
            player_keys=map(lambda p: p.key, players) if players is not None else [],
            game_key=game_key,
            starting_score=rules.startingScore if rules is not None else 0,
            scores=[]
        )

        game = Game(
            key=game_key,
            description=description,
            date=date,
            rules=rules,
            scoreHistory=score_history
        )

        return game
