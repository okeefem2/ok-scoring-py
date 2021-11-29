from ok_scoring.db.game_rules_mapper import game_rules
from ok_scoring.db.score_round_mapper import score_round
from ok_scoring.model.game_rules import GameRules
from ok_scoring.model.score_round import ScoreRound
from sqlalchemy.orm import mapper, relationship, clear_mappers

from ok_scoring.db.favorite_game_mapper import favorite_game
from ok_scoring.db.player_mapper import player
from ok_scoring.db.player_score_history_mapper import player_score_history
from ok_scoring.db.game_mapper import game
from ok_scoring.model.favorite_game import FavoriteGame
from ok_scoring.model.game import Game
from ok_scoring.model.player import Player
from ok_scoring.model.player_score_history import PlayerScoreHistory


def start_mappers():
    clear_mappers()
    game_rules_mapper = mapper(
        GameRules,
        game_rules
    )
    player_mapper = mapper(Player, player)
    score_rounds_mapper = mapper(
        ScoreRound,
        score_round,
    )
    player_score_history_mapper = mapper(
        PlayerScoreHistory,
        player_score_history,
        properties={
            'scores': relationship(
                ScoreRound,
                cascade='all, delete-orphan',
                lazy="joined",
                order_by=lambda: ScoreRound.order
            )
        },
    )
    game_mapper = mapper(
        Game,
        game,
        properties={
            'rules': relationship(
                GameRules,
                uselist=False,
                cascade='all, delete-orphan'
            ),
            'scoreHistory': relationship(
                PlayerScoreHistory,
                cascade='all, delete-orphan'
            ),
        },
    )
    favorite_game_mapper = mapper(FavoriteGame, favorite_game)

