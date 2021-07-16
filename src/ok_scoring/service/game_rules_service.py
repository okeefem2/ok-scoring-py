from math import inf

from ok_scoring.model.game_rules import GameRules
from ok_scoring.model.player import Player
from ok_scoring.model.player_score_history import PlayerScoreHistory
from ok_scoring.model.validation_error import ValidationError
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


class GameAlreadyWon(ValidationError):
    pass


# Pre game ######


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


def scores_meet_set_scores(set_scores, scores):
    # Check length first to short circuit the need to sort and create a new list
    return set_scores is not None and scores is not None \
           and len(set_scores) == len(scores) \
           and sorted(list(scores)) == sorted(list(set_scores))


# TODO this logic might be duplicated somewhere
def winning_score_met(winning_score, score, can_bust, high_score_wins):
    print('is winning score met', winning_score, score, can_bust, high_score_wins)
    if winning_score == score:
        return True
    # TODO maybe flip these names?... defaulting None to also be true is annoying
    if can_bust is True or can_bust is None:
        return winning_score < score \
            if high_score_wins or high_score_wins is None \
            else winning_score > score
    return False


def min_rounds_met(min_rounds_to_win, scores):
    return min_rounds_to_win is None \
                or min_rounds_to_win <= len(scores)


def game_complete(rules: GameRules, scoreHistory: [PlayerScoreHistory]):

    for playerScoreHistory in scoreHistory:
        # If player hasn't met the min rounds required, they can't have won
        if not min_rounds_met(rules.minRoundsToWin, playerScoreHistory.scores):
            continue
        # If one player has gotten all of the set scores, game is over
        if scores_meet_set_scores(rules.setScores, playerScoreHistory.scores):
            return True
        if winning_score_met(rules.winningScore, playerScoreHistory.currentScore, rules.canBust, rules.highScoreWins):
            return True

    return False


def validate_rounds(rules: GameRules, rounds, score_round):
    if score_round < len(rounds):
        return True
    num_new_rounds = score_round - len(rounds) + 1
    if rules.rounds is not None and len(rounds) + num_new_rounds > rules.rounds:
        raise ExceededRounds(
            propertyPath='game.scoreHistory',  # TODO key for the scoreHistory
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

    ## TODO look at these
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


# TODO might need to consider the order and round in which the winning score was met
def determine_winner(scoreHistory: [PlayerScoreHistory], rules: GameRules) -> str:
    high_score_wins = rules.highScoreWins if rules is not None else True

    winning_score = None

    for playerScore in scoreHistory:
        if winning_score is None \
                or score_beats_winner(high_score_wins, winning_score.currentScore, playerScore.currentScore):
            winning_score = playerScore


    # winning_score: PlayerScoreHistory = \
    #     max(scoreHistory, key=lambda s: s.currentScore if s.currentScore is not None else default_score) if high_score_wins is True \
    #     else min(scoreHistory, key=lambda s: s.currentScore if s.currentScore is not None else default_score)
    return winning_score.playerKey


# End game #####
