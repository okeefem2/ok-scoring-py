import unittest

from ok_scoring.model.game_rules import GameRules
from ok_scoring.model.player import Player
from ok_scoring.service.game_rules_service import validate_rounds, ExceededRounds, validate_score, ScoreBusts, \
    validate_player, \
    ExceededMaxPlayers, PlayerAlreadyExists, validate_players, MinPlayersNotMet, determine_winner, ScoreNotInSet, \
    build_new_game_rules, game_complete, scores_meet_set_scores, winning_score_met, min_rounds_met


# Pre game validations ######

class CreateGameRules(unittest.TestCase):

    def test_starting_score(self):
        rules = build_new_game_rules({'startingScore': 10})
        assert rules.startingScore == 10

    def test_ignore_adding_nonexistent_prop(self):
        rules = build_new_game_rules({'weight': 10})
        self.assertRaises(AttributeError, getattr, rules, 'weight')


class ValidatePlayer(unittest.TestCase):

    def test_cannot_add_player_over_max(self):
        rules = GameRules(key='key', maxPlayers=1)
        playerOne = Player(key='1', name='name1', favorite=False)
        playerTwo = Player(key='2', name='name2', favorite=False)
        players = [playerOne]
        self.assertRaises(ExceededMaxPlayers, validate_player, rules, players, playerTwo)

    def test_can_add_player_under_max(self):
        rules = GameRules(key='key', maxPlayers=2)
        playerOne = Player(key='1', name='name1', favorite=False)
        playerTwo = Player(key='2', name='name2', favorite=False)
        players = [playerOne]
        assert validate_player(rules, players, playerTwo) is True

    def test_cannot_add_player_already_exists(self):
        rules = GameRules(key='key', maxPlayers=3)
        playerOne = Player(key='1', name='name1', favorite=False)
        playerTwo = Player(key='2', name='name2', favorite=False)
        players = [playerOne, playerTwo]
        self.assertRaises(PlayerAlreadyExists, validate_player, rules, players, playerTwo)

    def test_can_add_player_does_not_exist(self):
        rules = GameRules(key='key')
        playerOne = Player(key='1', name='name1', favorite=False)
        playerTwo = Player(key='2', name='name2', favorite=False)
        players = [playerOne]
        assert validate_player(rules, players, playerTwo) is True


class ValidatePlayers(unittest.TestCase):

    def test_can_start_game_when_min_players_met(self):
        rules = GameRules(key='key', minPlayers=2)
        playerOne = Player(key='1', name='name1', favorite=False)
        playerTwo = Player(key='2', name='name2', favorite=False)
        players = [playerOne, playerTwo]
        assert validate_players(rules, players) is True

    def test_cannot_start_game_when_min_players_not_met(self):
        rules = GameRules(key='key', minPlayers=3)
        playerOne = Player(key='1', name='name1', favorite=False)
        playerTwo = Player(key='2', name='name2', favorite=False)
        players = [playerOne, playerTwo]
        self.assertRaises(MinPlayersNotMet, validate_players, rules, players)

# During game validations #####


class TestMinRoundsMet(unittest.TestCase):

    def test_if_no_min_rounds_set(self):
        assert min_rounds_met(None, [1, 2, 3, 4]) is True
        assert min_rounds_met(0, [1, 2, 3, 4]) is True

    def test_if_min_rounds_met(self):
        assert min_rounds_met(4, [1, 2, 3, 4]) is True

    def test_if_min_rounds_not_met(self):
        assert min_rounds_met(4, [1, 2, 3]) is False


class TestWinningScoreMet(unittest.TestCase):

    def test_if_score_is_winning_score_high(self):
        assert winning_score_met(100, 100, True, True) is True

    def test_if_score_is_winning_score_low(self):
        assert winning_score_met(100, 100, True, False) is True

    def test_if_score_is_less_than_winning_score_high(self):
        assert winning_score_met(100, 90, True, True) is False

    def test_if_score_is_less_than_winning_score_low(self):
        assert winning_score_met(100, 90, True, False) is True

    def test_if_score_is_greater_than_winning_score_high(self):
        assert winning_score_met(100, 110, True, True) is True

    def test_if_score_is_greater_than_winning_score_low(self):
        assert winning_score_met(100, 110, True, False) is False

    def test_if_score_busts_high(self):
        assert winning_score_met(100, 110, False, True) is False

    def test_if_score_busts_low(self):
        assert winning_score_met(100, 90, False, False) is False


class TestScoresMeetSetScores(unittest.TestCase):

    def test_if_player_meets_set_score_in_order(self):
        scores_met = scores_meet_set_scores({1, 2, 3, 4}, [1, 2, 3, 4])
        assert scores_met is True

    def test_if_player_meets_set_score_out_of_order(self):
        scores_met = scores_meet_set_scores({1, 2, 3, 4}, [4, 3, 2, 1])
        assert scores_met is True

    def test_if_no_set_scores(self):
        scores_met = scores_meet_set_scores(None, [4, 3, 2, 1])
        assert scores_met is False

    def test_if_no_scores(self):
        scores_met = scores_meet_set_scores({1, 2, 3, 4}, None)
        assert scores_met is False

    def test_if_scores_not_met(self):
        scores_met = scores_meet_set_scores({1, 2, 3, 4}, [1, 3, 4])
        assert scores_met is False


class TestValidateRounds(unittest.TestCase):

    def test_can_add_score_for_player_under_round_cap(self):
        rules = GameRules(key='key', rounds=5)
        assert validate_rounds(rules, [1, 2, 3], 3) is True

    def test_can_add_score_for_player_meeting_round_cap(self):
        rules = GameRules(key='key', rounds=4)
        assert validate_rounds(rules, [1, 2, 3], 3) is True

    def test_cannot_add_score_for_player_at_round_cap(self):
        rules = GameRules(key='key', rounds=3)
        self.assertRaises(ExceededRounds, validate_rounds, rules, [1, 2, 3], 3)


class TestValidateScore(unittest.TestCase):
    def test_cannot_add_score_for_player_that_busts_positive(self):
        rules = GameRules(key='key', canBust=True, winningScore=5, highScoreWins=True)
        self.assertRaises(ScoreBusts, validate_score, rules, 1, 6)

    def test_cannot_add_score_for_player_that_busts_negative(self):
        rules = GameRules(key='key', canBust=True, winningScore=0, highScoreWins=False)
        self.assertRaises(ScoreBusts, validate_score, rules, 1, -6)

    def test_can_add_score_if_in_set(self):
        rules = GameRules(key='key', setScores={1, 3, 5, 9})
        assert validate_score(rules, 1, 3) is True

    def test_cannot_add_score_if_not_in_set(self):
        rules = GameRules(key='key', setScores={1, 3, 5, 9})
        self.assertRaises(ScoreNotInSet, validate_score, rules, 1, 2)

#
# class TestDetermineWinner(unittest.TestCase):
#     def test_no_winner_if_no_rounds(self):
#         rules = GameRules(key='key', highScoreWins=True)
#         playerOneScores = PlayerScoreHistory(key='one', currentScore=0, scores=[], playerKey='1', gameKey='1', order=0)
#         playerTwoScores = PlayerScoreHistory(key='two', currentScore=0, scores=[], playerKey='2', gameKey='1', order=1)
#         scoreHistory = {'one': playerOneScores, 'two': playerTwoScores}
#
#         assert determine_winner(rules, scoreHistory) is None
#
#     def test_winner_if_score_higher(self):
#         rules = GameRules(key='key', highScoreWins=True)
#         playerOneScores = PlayerScoreHistory(key='one', currentScore=10, scores=[5, 5], playerKey='1', gameKey='1', order=0)
#         playerTwoScores = PlayerScoreHistory(key='two', currentScore=3, scores=[3], playerKey='2', gameKey='1', order=1)
#         scoreHistory = {'one': playerOneScores, 'two': playerTwoScores}
#
#         assert determine_winner(rules, scoreHistory) == 'one'
#
#     def test_winner_if_score_lower(self):
#         rules = GameRules(key='key', highScoreWins=False)
#         playerOneScores = PlayerScoreHistory(key='one', currentScore=10, scores=[5, 5], playerKey='1', gameKey='1', order=0)
#         playerTwoScores = PlayerScoreHistory(key='two', currentScore=3, scores=[3], playerKey='2', gameKey='1', order=1)
#         scoreHistory = {'one': playerOneScores, 'two': playerTwoScores}
#
#         assert determine_winner(rules, scoreHistory) == 'two'
#
#     def test_winner_if_default(self):
#         rules = GameRules(key='key')
#         playerOneScores = PlayerScoreHistory(key='one', currentScore=10, scores=[5, 5], playerKey='1', gameKey='1', order=0)
#         playerTwoScores = PlayerScoreHistory(key='two', currentScore=3, scores=[3], playerKey='2', gameKey='1', order=1)
#         scoreHistory = {'one': playerOneScores, 'two': playerTwoScores}
#
#         assert determine_winner(rules, scoreHistory) == 'one'


if __name__ == '__main__':
    unittest.main()
