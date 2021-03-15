from sqlalchemy import MetaData
from sqlalchemy.orm import mapper, relationship

from src.db.favorite_game_mapper import favorite_game
from src.db.game_rules_mapper import game_rules
from src.db.player_mapper import player
from src.db.player_score_history_mapper import player_score_history
from src.model import game
from src.model.favoriteGame import FavoriteGame
from src.model.game import Game
from src.model.gameRules import GameRules
from src.model.player import Player
from src.model.playerScoreHistory import PlayerScoreHistory

metadata = MetaData()


def start_mappers():
    game_rules_mapper = mapper(
        GameRules,
        game_rules
    )
    player_mapper = mapper(Player, player)
    player_score_history_mapper = mapper(
        PlayerScoreHistory,
        player_score_history,
    )
    game_mapper = mapper(
        Game,
        game,
        properties={
            'rules': relationship(
                game_rules_mapper
            ),
            'scores': relationship(
                player_score_history_mapper, collection_class=set
            ),
        },
    )
    favorite_game_mapper = mapper(FavoriteGame, favorite_game)

