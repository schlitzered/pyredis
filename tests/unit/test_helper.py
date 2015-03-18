__author__ = 'schlitzer'

from unittest import TestCase

from pyredis.helper import dict_from_list


class TestHelperUnit(TestCase):
    def test_dict_from_list(self):
        source = ['test1', 1234, 'test2', 5678]
        expected = {
            'test1': 1234,
            'test2': 5678
        }
        result = dict_from_list(source)
        self.assertEqual(result, expected)
