from service.game_rules_service import validate_rounds, validate_score


def can_add_player_round(game, playerKey: str, score: int) -> bool:
    # Maybe could have a rule to add the player if they do not exist
    if playerKey not in game.scoreHistory:
        return False
    if game.rules is None:  # NO RULES!!
        return True

    playerScoreHistory = game.scoreHistory[playerKey]
    return validate_rounds(game.rules, len(playerScoreHistory.scores)) \
           and validate_score(game.rules, playerScoreHistory.currentScore, score)
