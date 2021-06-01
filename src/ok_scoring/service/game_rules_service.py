from math import inf

from ok_scoring.model.game_rules import GameRules
from ok_scoring.model.player import Player
from ok_scoring.model.player_score_history import PlayerScoreHistory
from ok_scoring.model.validation_error import ValidationError
from ok_scoring.repository.abstract_repository import AbstractRepository
from ok_scoring.repository.helpers import unique_id


class ExceededMaxPlayers(ValidationError):
    pass


class MinPlayersNotMet(ValidationError):
    pass


class PlayerAlreadyExists(ValidationError):
    pass


class ExceededRounds(ValidationError):
    pass


class ScoreBusts(ValidationError):
    pass


class ScoreNotInSet(ValidationError):
    pass


class ScoreSignInvalid(ValidationError):
    pass


# Pre game ######

def create_game_rules(repo: AbstractRepository, rules_dict: dict) -> GameRules:
    rules = build_new_game_rules(rules_dict)
    repo.add(rules)
    return rules


# TODO validate game rules properties
def build_new_game_rules(rules_dict: dict) -> GameRules:
    rules = GameRules(key=unique_id())
    if type(rules_dict) is dict:
        for key in rules_dict:
            if hasattr(rules, key):
                setattr(rules, key, rules_dict[key])
    return rules


def validate_players(rules: GameRules, players: [Player]):
    if rules is not None \
            and rules.minPlayers is not None \
            and rules.minPlayers > len(players):
        raise MinPlayersNotMet(
            propertyPath=f'game.players',
            errorType='minLength',
            errorMessage=f'Minimum number of players not met {rules.minPlayers}'
        )
    return True


def validate_player(rules: GameRules, players: [Player], player: Player):
    if rules.maxPlayers is not None and rules.maxPlayers < len(players) + 1:
        raise ExceededMaxPlayers(
            propertyPath='game.players',
            errorType='invalid',
            errorMessage=f'Max number of players already met {rules.maxPlayers}'
        )
    playerAlreadyExists = next((True for p in players if p == player), False)
    if playerAlreadyExists:
        raise PlayerAlreadyExists(
            propertyPath=f'game.players[{player.key}]',
            errorType='duplicate',
            errorMessage=f'Player with key {player.key} already exists'
        )
    return True


# During game #####


def validate_rounds(rules: GameRules, rounds):
    if rules.rounds is not None and rounds + 1 > rules.rounds:
        raise ExceededRounds(
            propertyPath='game.scoreHistory', # TODO key for the scoreHistory
            errorType='invalid',
            errorMessage=f'Max number of rounds already met {rules.rounds}'
        )
    return True


def validate_score(rules: GameRules, current_score, round_score):
    if rules.setScores and round_score not in rules.setScores:
        raise ScoreNotInSet(
            propertyPath='game.scoreHistory',  # TODO key for the scoreHistory
            errorType='invalid',
            errorMessage=f'{round_score} is not a valid score'
        )
    if rules.canBust and rules.highScoreWins and current_score + round_score > rules.winningScore:
        raise ScoreBusts(
            propertyPath='game.scoreHistory',  # TODO key for the scoreHistory
            errorType='invalid',
            errorMessage=f'Score cannot exceed {rules.winningScore}'
        )
    if rules.canBust and not rules.highScoreWins and current_score + round_score < rules.winningScore:
        raise ScoreBusts(
            propertyPath='game.scoreHistory',  # TODO key for the scoreHistory
            errorType='invalid',
            errorMessage='Score cannot be lower than {rules.winningScore}')

    return True


def score_beats_winner(highScoreWins, winningScore, score):
    return score > winningScore if highScoreWins else score < winningScore


def determine_winner(rules: GameRules, scoreHistory: dict[str, PlayerScoreHistory]):
    highScoreWins = rules.highScoreWins is True or rules.highScoreWins is None
    winningScore = -inf if highScoreWins else inf
    winningPlayerKey = None
    if len(scoreHistory.keys()) > 0:
        for playerKey, playerScores in scoreHistory.items():
            if len(playerScores.scores) > 0 and \
                    score_beats_winner(highScoreWins, winningScore, playerScores.currentScore):
                winningScore = playerScores.currentScore
                winningPlayerKey = playerKey
    return winningPlayerKey


# End game #####
