from typing import Optional

import dataclasses
import jsonschema_rs
from ok_scoring.model.dealer_settings import DealerSettings
from ok_scoring.model.game import Game
from ok_scoring.model.game_rules import GameRules
from ok_scoring.model.player_score_history import PlayerScoreHistory
from ok_scoring.service.player_score_history_service import find_by_player_key, find_by_order_index
from ok_scoring.repository.helpers import unique_id


def build_new_game_rules(rules_dict: dict) -> GameRules:
    rules = GameRules(key=unique_id())
    if type(rules_dict) is dict:
        for key in rules_dict:
            if hasattr(rules, key):
                setattr(rules, key, rules_dict[key])
    return rules


def convert_score_history_to_dict(score_history: [PlayerScoreHistory]) -> dict:
    # score_history_dict = [dataclasses.asdict(s) for s in score_history] if score_history is not None else []
    s = []
    for player_score_history in score_history:
        player_score_history_dict = dataclasses.asdict(player_score_history)
        player_score_history_dict['scores'] = [s for s in player_score_history_dict['scores']]
        s.append(player_score_history_dict)
    return {'scoreHistory': s}


def validate_game_state(game: Game):
    schema = game.rules.validStateSchema
    score_history = game.scoreHistory

    # this is where JS would probably win out nicely in efficiency
    jsonschema_rs.validate(schema, convert_score_history_to_dict(score_history))
    return True


def is_game_won(game: Game) -> bool:
    schema = game.rules.winningSchema

    score_history = game.scoreHistory

    # this is where JS would probably win out nicely in efficiency
    return jsonschema_rs.is_valid(schema, convert_score_history_to_dict(score_history))


# Rules that cannot be captured with json schema currently


def can_add_round(round_index: int, player_score_history: PlayerScoreHistory, game: Game) -> bool:
    return round_index >= len(player_score_history.scores) and is_game_won(game)


def score_beats_winner(highScoreWins, winningScore, score):
    return score > winningScore if highScoreWins else score < winningScore


# TODO might need to consider the order and round in which the winning score was met
def determine_winner(scoreHistory: [PlayerScoreHistory], rules: GameRules) -> str:
    high_score_wins = rules.highScoreWins if rules is not None else True
    winning_score = None

    for playerScore in scoreHistory:
        if len(playerScore.scores) > 0 and \
                (
                        winning_score is None
                        or score_beats_winner(high_score_wins, winning_score.currentScore, playerScore.currentScore)
                ):
            winning_score = playerScore

    return winning_score.playerKey if winning_score is not None else None


def determine_next_dealer(scoreHistory: [PlayerScoreHistory], rules: GameRules, currentDealerKey: Optional[str]):
    if rules.dealerSettings != DealerSettings.NewPerRound:
        return currentDealerKey

    currentDealer: PlayerScoreHistory = find_by_player_key(scoreHistory, currentDealerKey)
    nextDealerIndex = currentDealer.order + 1 \
        if currentDealer is not None and currentDealer.order < len(scoreHistory) - 1 \
        else 0
    nextDealer: PlayerScoreHistory = find_by_order_index(scoreHistory, nextDealerIndex)
    return nextDealer.playerKey
