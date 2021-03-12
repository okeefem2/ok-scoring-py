from src.service.game_rules_service import validate_rounds, validate_score

# Create a builder function
from src.service.player_score_history_service import set_round_score


def add_player_round(game, playerKey: str, score: int, round_index: int):
    if can_add_player_round(game, playerKey, score):
        set_round_score(game.scoreHistory[playerKey], score, round_index)


def can_add_player_round(game, playerKey: str, score: int) -> bool:
    # Maybe could have a rule to add the player if they do not exist
    if playerKey not in game.scoreHistory:
        return False
    if game.rules is None:  # NO RULES!!
        return True

    playerScoreHistory = game.scoreHistory[playerKey]
    return validate_rounds(game.rules, len(playerScoreHistory.scores)) \
           and validate_score(game.rules, playerScoreHistory.currentScore, score)
