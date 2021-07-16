import unittest

from ok_scoring.model.player import Player
from ok_scoring.service.player_service import build_new_player, filter_out_existing_names


class TestCreatePlayer(unittest.TestCase):
    def test_new_player_has_id_and_name_and_favorite(self):
        player = build_new_player('Roland')
        assert player.name == 'Roland'
        assert player.key is not None
        assert player.favorite is False


class TestFilterOutExistingNames(unittest.TestCase):

    def test_no_existing_players(self):
        assert filter_out_existing_names(None, ['Dracula', 'Alucard']) == ['Dracula', 'Alucard']
        assert filter_out_existing_names([], ['Dracula', 'Alucard']) == ['Dracula', 'Alucard']

    def test_existing_player_no_match(self):
        result = filter_out_existing_names([Player(key='1', name='Carmilla')], ['Dracula', 'Alucard'])
        assert result == ['Dracula', 'Alucard']

    def test_existing_player_match(self):
        result = filter_out_existing_names([Player(key='1', name='Dracula')], ['Dracula', 'Alucard'])
        assert result == ['Alucard']

    def test_existing_player_all_match(self):
        result = filter_out_existing_names([Player(key='1', name='Dracula'), Player(key='2', name='Alucard')], ['Dracula', 'Alucard'])
        assert result == []

# TODO integration test
# class TestCreatePlayers(unittest.TestCase):
#     def test_new_players(self):
#         players = create_players(['Roland', 'Eddie', 'Susannah', 'Jake', 'Oy'])
#         assert len(players) == 5

if __name__ == '__main__':
    unittest.main()
