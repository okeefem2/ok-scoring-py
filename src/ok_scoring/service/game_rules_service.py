from math import inf

from ok_scoring.model.game_rules import GameRules
from ok_scoring.model.player import Player
from ok_scoring.model.player_score_history import PlayerScoreHistory
from ok_scoring.repository.helpers import unique_id


class ExceededMaxPlayers(Exception):
    pass


class MinPlayersNotMet(Exception):
    pass


class PlayerAlreadyExists(Exception):
    pass


class ExceededRounds(Exception):
    pass


class ScoreBusts(Exception):
    pass


class ScoreNotInSet(Exception):
    pass


class ScoreSignInvalid(Exception):
    pass


# Pre game ######

# TODO validate game rules properties
def create_game_rules(rules_dict: dict) -> GameRules:
    rules = GameRules(key=unique_id())
    for key in rules_dict:
        if hasattr(rules, key):
            setattr(rules, key, rules_dict[key])
    return rules


def validate_players(rules: GameRules, players: [Player]):
    if rules is not None \
            and rules.minPlayers is not None \
            and rules.minPlayers > len(players):
        raise MinPlayersNotMet
    return True


def validate_player(rules: GameRules, players: [Player], player: Player):
    if rules.maxPlayers is not None and rules.maxPlayers < len(players) + 1:
        raise ExceededMaxPlayers(f'Max number of players already met {rules.maxPlayers}')
    playerAlreadyExists = next((True for p in players if p == player), False)
    if playerAlreadyExists:
        raise PlayerAlreadyExists(f'Player with key {player.key} already exists')
    return True


def build_player_score_history(rules: GameRules, players: [Player], gameKey: str) -> {str, PlayerScoreHistory}:
    playerScoreHistory = {}
    startingScore = rules.startingScore if rules.startingScore else 0
    for player in players:
        playerScoreHistory[player.key] = PlayerScoreHistory(
            currentScore=startingScore,
            scores=[],
            playerKey=player.key,
            gameKey=gameKey
        )
    return playerScoreHistory


# During game #####


def validate_rounds(rules: GameRules, rounds):
    if rules.rounds is not None and rounds + 1 > rules.rounds:
        raise ExceededRounds(f'Max number of rounds already met {rules.rounds}')
    return True


def validate_score(rules: GameRules, current_score, round_score):
    if rules.setScores and round_score not in rules.setScores:
        raise ScoreNotInSet(f'{round_score} is not a valid score')
    if rules.canBust and rules.highScoreWins and current_score + round_score > rules.winningScore:
        raise ScoreBusts(f'Score cannot exceed {rules.winningScore}')
    if rules.canBust and not rules.highScoreWins and current_score + round_score < rules.winningScore:
        raise ScoreBusts(f'Score cannot be lower than {rules.winningScore}')

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