import time

from ok_scoring.model.game import Game
from ok_scoring.model.game_rules import GameRules
from ok_scoring.model.player import Player
from ok_scoring.model.player_score_history import PlayerScoreHistory
from ok_scoring.model.validation_error import ValidationError
from ok_scoring.repository.helpers import unique_id, now

# Create a builder function
from ok_scoring.service.game_rules_service import validate_rounds, validate_score, validate_players, determine_winner, \
    determine_next_dealer
from ok_scoring.service.player_score_history_service import set_round_score, build_score_history, is_round_complete, \
    is_current_round


class DescriptionRequired(ValidationError):
    pass


class RoundNotValid(ValidationError):
    pass


# TODO probably need to compare previous game state to new game state
def update_dealer(new_game: Game, previous_score_history: [PlayerScoreHistory], round_index):
    # TODO only update dealer if new round completes current round
    # TODO this raises the question of if we should allow a player to have rounds way ahead of another player...

    if is_current_round(new_game.scoreHistory, round_index) \
            and is_round_complete(new_game.scoreHistory, round_index) \
            and not is_round_complete(previous_score_history, round_index):
        new_game.dealingPlayerKey = \
            determine_next_dealer(new_game.scoreHistory, new_game.rules, new_game.dealingPlayerKey)
    return new_game


def update_winner(game):
    game.winningPlayerKey = determine_winner(scoreHistory=game.scoreHistory, rules=game.rules)
    return game


def validate_and_set_round_score(score_history: PlayerScoreHistory, rules: GameRules, score: int, round_index: int, score_index: int):
    if can_add_player_round(scoreHistory=score_history, rules=rules, score=score, round_index=round_index):
        score_history = set_round_score(score_history, score, round_index, score_index=score_index)
    else:
        raise RoundNotValid(propertyPath=f'game.scoreHistory{{playerKey={score_history.playerKey}}}[{round_index}]',
                            errorType='invalid',
                            errorMessage='Score invalid')

    return score_history


def can_add_player_round(scoreHistory: PlayerScoreHistory, rules, score: int, round_index: int) -> bool:
    if rules is None:  # NO RULES!!
        return True

    return validate_rounds(rules, scoreHistory.scores, round_index) \
           and validate_score(rules, scoreHistory.currentScore, score)


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
