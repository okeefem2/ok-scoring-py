import unittest

from src.service.player_service import create_player, create_players


class TestCreatePlayer(unittest.TestCase):
    def test_new_player_has_id_and_name_and_favorite(self):
        player = create_player('Roland')
        assert player.name == 'Roland'
        assert player.key is not None
        assert player.favorite is False


class TestCreatePlayers(unittest.TestCase):
    def test_new_players(self):
        players = create_players(['Roland', 'Eddie', 'Susannah', 'Jake', 'Oy'])
        assert len(players) == 5

    # TODO should test existing players with mock repo


if __name__ == '__main__':
    unittest.main()
