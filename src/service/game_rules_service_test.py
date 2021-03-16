import unittest

from src.model.gameRules import GameRules
from src.model.player import Player
from src.model.playerScoreHistory import PlayerScoreHistory
from src.service.game_rules_service import validate_rounds, ExceededRounds, validate_score, ScoreBusts, validate_player, \
    ExceededMaxPlayers, PlayerAlreadyExists, validate_players, MinPlayersNotMet, determine_winner, ScoreNotInSet, \
    build_player_score_history, create_game_rules


# Pre game validations ######

class CreateGameRules(unittest.TestCase):

    def test_starting_score(self):
        rules = create_game_rules({'startingScore': 10})
        assert rules.startingScore == 10

    def test_ignore_adding_nonexistent_prop(self):
        rules = create_game_rules({'weight': 10})
        self.assertRaises(AttributeError, getattr, rules, 'weight')


class ValidatePlayer(unittest.TestCase):

    def test_cannot_add_player_over_max(self):
        rules = GameRules(key="key", maxPlayers=1)
        playerOne = Player(key="1", 'name2', favorite=False)
        playerTwo = Player(key="2", name='name2', favorite=False)
        players = [playerOne]
        self.assertRaises(ExceededMaxPlayers, validate_player, rules, players, playerTwo)

    def test_can_add_player_under_max(self):
        rules = GameRules(key="key", maxPlayers=2)
        playerOne = Player(key="1")
        playerTwo = Player(key="2")
        players = [playerOne]
        assert validate_player(rules, players, playerTwo) is True

    def test_cannot_add_player_already_exists(self):
        rules = GameRules(key="key", maxPlayers=2)
        playerOne = Player(key="1")
        playerTwo = Player(key="1")
        players = [playerOne]
        self.assertRaises(PlayerAlreadyExists, validate_player, rules, players, playerTwo)

    def test_can_add_player_does_not_exist(self):
        rules = GameRules(key="key")
        playerOne = Player(key="1")
        playerTwo = Player(key="2")
        players = [playerOne]
        assert validate_player(rules, players, playerTwo) is True


class ValidatePlayers(unittest.TestCase):

    def test_can_start_game_when_min_players_met(self):
        rules = GameRules(key="key", minPlayers=2)
        playerOne = Player(key="1")
        playerTwo = Player(key="2")
        players = [playerOne, playerTwo]
        assert validate_players(rules, players) is True

    def test_cannot_start_game_when_min_players_not_met(self):
        rules = GameRules(key="key", minPlayers=3)
        playerOne = Player(key="1")
        playerTwo = Player(key="2")
        players = [playerOne, playerTwo]
        self.assertRaises(MinPlayersNotMet, validate_players, rules, players)


class BuildPlayerScoreHistory(unittest.TestCase):

    def test_player_score_historys_should_have_default_starting_score(self):
        rules = GameRules(key='key', startingScore=100)
        playerOne = Player(key='one')
        playerTwo = Player(key='two')
        playerScoreHistory = build_player_score_history(rules, [playerOne, playerTwo])
        assert playerScoreHistory['one'].currentScore == 100
        assert playerScoreHistory['two'].currentScore == 100

    def test_player_score_historys_should_start_at_zero_if_no_default_starting_score(self):
        rules = GameRules(key='key')
        playerOne = Player(key='one')
        playerTwo = Player(key='two')
        playerScoreHistory = build_player_score_history(rules, [playerOne, playerTwo])
        assert playerScoreHistory['one'].currentScore == 0
        assert playerScoreHistory['two'].currentScore == 0


# During game validations #####


class TestValidateRounds(unittest.TestCase):

    def test_can_add_score_for_player_under_round_cap(self):
        rules = GameRules(key="key", rounds=5)
        assert validate_rounds(rules, 3) is True

    def test_can_add_score_for_player_meeting_round_cap(self):
        rules = GameRules(key="key", rounds=4)
        assert validate_rounds(rules, 3) is True

    def test_cannot_add_score_for_player_at_round_cap(self):
        rules = GameRules(key="key", rounds=3)
        self.assertRaises(ExceededRounds, validate_rounds, rules, 3)


class TestValidateScore(unittest.TestCase):
    def test_cannot_add_score_for_player_that_busts_positive(self):
        rules = GameRules(key="key", canBust=True, winningScore=5, highScoreWins=True)
        self.assertRaises(ScoreBusts, validate_score, rules, 1, 6)

    def test_cannot_add_score_for_player_that_busts_negative(self):
        rules = GameRules(key="key", canBust=True, winningScore=0, highScoreWins=False)
        self.assertRaises(ScoreBusts, validate_score, rules, 1, -6)

    def test_can_add_score_if_in_set(self):
        rules = GameRules(key="key", setScores={1, 3, 5, 9})
        assert validate_score(rules, 1, 3) is True

    def test_cannot_add_score_if_not_in_set(self):
        rules = GameRules(key="key", setScores={1, 3, 5, 9})
        self.assertRaises(ScoreNotInSet, validate_score, rules, 1, 2)


class TestDetermineWinner(unittest.TestCase):
    def test_no_winner_if_no_rounds(self):
        rules = GameRules(key="key", highScoreWins=True)
        playerOneScores = PlayerScoreHistory(key="one", currentScore=0, scores=[])
        playerTwoScores = PlayerScoreHistory(key="two", currentScore=0, scores=[])
        scoreHistory = {"one": playerOneScores, "two": playerTwoScores}

        assert determine_winner(rules, scoreHistory) is None

    def test_winner_if_score_higher(self):
        rules = GameRules(key="key", highScoreWins=True)
        playerOneScores = PlayerScoreHistory(key="one", currentScore=10, scores=[5, 5])
        playerTwoScores = PlayerScoreHistory(key="two", currentScore=3, scores=[3])
        scoreHistory = {"one": playerOneScores, "two": playerTwoScores}

        assert determine_winner(rules, scoreHistory) == "one"

    def test_winner_if_score_lower(self):
        rules = GameRules(key="key", highScoreWins=False)
        playerOneScores = PlayerScoreHistory(key="one", currentScore=10, scores=[5, 5])
        playerTwoScores = PlayerScoreHistory(key="two", currentScore=3, scores=[3])
        scoreHistory = {"one": playerOneScores, "two": playerTwoScores}

        assert determine_winner(rules, scoreHistory) == "two"

    def test_winner_if_default(self):
        rules = GameRules(key="key")
        playerOneScores = PlayerScoreHistory(key="one", currentScore=10, scores=[5, 5])
        playerTwoScores = PlayerScoreHistory(key="two", currentScore=3, scores=[3])
        scoreHistory = {"one": playerOneScores, "two": playerTwoScores}

        assert determine_winner(rules, scoreHistory) == "one"


if __name__ == '__main__':
    unittest.main()
