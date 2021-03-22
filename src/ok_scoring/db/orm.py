from sqlalchemy.orm import mapper, relationship

from ok_scoring.favorite_game_mapper import favorite_game
from ok_scoring.db.game_rules_mapper import game_rules
from ok_scoring.db.player_mapper import player
from ok_scoring.db.player_score_history_mapper import player_score_history
from ok_scoring.db.game_mapper import game
from ok_scoring.model.favorite_game import FavoriteGame
from ok_scoring.model.game import Game
from ok_scoring.model.game_rules import GameRules
from ok_scoring.model.player import Player
from ok_scoring.model.player_score_history import PlayerScoreHistory

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

