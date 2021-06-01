import unittest

from ok_scoring.service.player_service import create_player, create_players


class TestCreatePlayer(unittest.TestCase):
    def test_new_player_has_id_and_name_and_favorite(self):
        player = create_player('Roland')
        assert player.name == 'Roland'
        assert player.key is not None
        assert player.favorite is False


# TODO integration test
# class TestCreatePlayers(unittest.TestCase):
#     def test_new_players(self):
#         players = create_players(['Roland', 'Eddie', 'Susannah', 'Jake', 'Oy'])
#         assert len(players) == 5

if __name__ == '__main__':
    unittest.main()
