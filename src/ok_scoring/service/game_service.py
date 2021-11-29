import time

from ok_scoring.model.game import Game
from ok_scoring.model.game_rules import GameRules
from ok_scoring.model.game_rules import GameRules
from ok_scoring.model.player import Player
from ok_scoring.model.player_score_history import PlayerScoreHistory
from ok_scoring.model.validation_error import OKValidationError
from ok_scoring.repository.helpers import unique_id, now
from ok_scoring.service.game_rules_service import determine_winner, determine_next_dealer
from ok_scoring.service.player_score_history_service import set_round_score, build_score_history, is_round_complete, \
    is_current_round


class DescriptionRequired(OKValidationError):
    pass


class RoundNotValid(OKValidationError):
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


def build_new_game(description: str, players: [Player] = None, rules: GameRules = None) -> Game:
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
        # TODO Need to figure out the starting score piece here
        # starting_score=rules.startingScore if rules is not None else 0,
        starting_score=0,
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
