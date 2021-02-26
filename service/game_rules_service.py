from model.game_rules import GameRules


class ExceededRounds(Exception):
    pass


class ScoreBusts(Exception):
    pass


def validate_rounds(rules: GameRules, rounds):
    if rules.rounds is not None and rounds + 1 > rules.rounds:
        raise ExceededRounds(f'Max number of rounds already met {rules.rounds}')
    return True


def validate_score(rules: GameRules, current_score, round_score):
    if rules.canBust and rules.highScoreWins and current_score + round_score > rules.winningScore:
        raise ScoreBusts(f'Score cannot exceed {rules.winningScore}')
    if rules.canBust and not rules.highScoreWins and current_score + round_score < rules.winningScore:
        raise ScoreBusts(f'Score cannot be lower than {rules.winningScore}')
    return True
