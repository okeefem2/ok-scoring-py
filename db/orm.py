from sqlalchemy.orm import mapper

from db.favoriteGameMapper import favoriteGame
from db.gameRulesMapper import gameRules
from db.playerMapper import player
from db.playerScoreHistoryMapper import playerScoreHistory
from model import game
from model.favoriteGame import FavoriteGame
from model.game import Game
from model.gameRules import GameRules
from model.player import Player
from model.playerScoreHistory import PlayerScoreHistory


def startMappers():
    gameRulesMapper = mapper(GameRules, gameRules)
    favoriteGameMapper = mapper(FavoriteGame, favoriteGame)
    gameMapper = mapper(Game, game)
    playerMapper = mapper(Player, player)
    playerScoreHistoryMapper = mapper(PlayerScoreHistory, playerScoreHistory)
