import unittest

from ok_scoring.utils.list.update_and_copy_list import update_and_copy_list


class TestUpdateAndCopyList(unittest.TestCase):
    def test_index_error_greater_than_length(self):
        self.assertRaises(IndexError, update_and_copy_list, [1, 2], 3, 2)

    def test_index_error_less_than_zero(self):
        self.assertRaises(IndexError, update_and_copy_list, [1, 2], 3, -2)

    def test_updates_index(self):
        result = update_and_copy_list([1, 2], 3, 1)
        assert result == [1, 3]

    def test_new_list_new_reference(self):
        items = [1, 2]
        result = update_and_copy_list(items, 3, 1)
        assert result is not items
        assert result != items
        assert items == [1, 2]
        assert result == [1, 3]


if __name__ == '__main__':
    unittest.main()
