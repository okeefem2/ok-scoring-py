import unittest

from dataclasses import dataclass
from ok_scoring.utils.list.fill_missing_indexes_to_length import fill_missing_indexes_to_length


class TestFillMissingIndexes(unittest.TestCase):

    def test_no_fill_needed(self):
        assert fill_missing_indexes_to_length([1, 2, 4], 2, lambda: 0) == [1, 2, 4]
        assert fill_missing_indexes_to_length([1, 2, 4], 3, lambda: 0) == [1, 2, 4]

    def test_new_list_new_reference(self):
        items = [1, 2, 4]
        result = fill_missing_indexes_to_length(items, 4, lambda: 0)
        assert items is not result
        assert items != result
        assert items == [1, 2, 4]
        assert result == [1, 2, 4, 0]

    def test_fill_ints(self):
        assert fill_missing_indexes_to_length([1, 2, 4], 5, lambda: 0) == [1, 2, 4, 0, 0]

    def test_fill_class(self):
        @dataclass()
        class TestClass:
            value: int

        assert fill_missing_indexes_to_length([TestClass(value=1)], 2, lambda: TestClass(value=0)) \
               == [TestClass(value=1), TestClass(value=0)]

    def test_fill_class_with_new_instances(self):
        @dataclass()
        class TestClass:
            value: int

        class_list = fill_missing_indexes_to_length([TestClass(value=1)], 3, lambda: TestClass(value=0))
        assert class_list[1] is not class_list[2]


if __name__ == '__main__':
    unittest.main()
