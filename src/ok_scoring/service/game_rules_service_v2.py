from typing import Optional

import dataclasses
import jsonschema_rs
from ok_scoring.model.dealer_settings import DealerSettings
from ok_scoring.model.game import Game
from ok_scoring.model.game_rules_v2 import GameRulesV2
from ok_scoring.model.player_score_history import PlayerScoreHistory
from ok_scoring.service.player_score_history_service import find_by_player_key, find_by_order_index


def validate_game_state(game: Game):
    schema = game.rulesV2.validStateSchema
    score_history = game.scoreHistory

    # this is where JS would probably win out nicely in efficiency
    score_history_dict = [dataclasses.asdict(s) for s in score_history] if score_history is not None else []
    jsonschema_rs.validate(schema, {'scoreHistory': score_history_dict})
    return True


def is_game_won(game: Game) -> bool:
    schema = game.rulesV2.winningSchema
    score_history = game.scoreHistory

    # this is where JS would probably win out nicely in efficiency
    score_history_dict = [dataclasses.asdict(s) for s in score_history] if score_history is not None else []
    return jsonschema_rs.is_valid(schema, {'scoreHistory': score_history_dict})


# Rules that cannot be captured with json schema currently

def score_beats_winner(highScoreWins, winningScore, score):
    return score > winningScore if highScoreWins else score < winningScore


# TODO might need to consider the order and round in which the winning score was met
def determine_winner(scoreHistory: [PlayerScoreHistory], rules: GameRulesV2) -> str:
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


def determine_next_dealer(scoreHistory: [PlayerScoreHistory], rules: GameRulesV2, currentDealerKey: Optional[str]):
    if rules.dealerSettings != DealerSettings.NewPerRound:
        return currentDealerKey

    currentDealer: PlayerScoreHistory = find_by_player_key(scoreHistory, currentDealerKey)
    nextDealerIndex = currentDealer.order + 1 \
        if currentDealer is not None and currentDealer.order < len(scoreHistory) - 1 \
        else 0
    nextDealer: PlayerScoreHistory = find_by_order_index(scoreHistory, nextDealerIndex)
    return nextDealer.playerKey
