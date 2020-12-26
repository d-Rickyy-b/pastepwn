# -*- coding: utf-8 -*-
import unittest
from unittest.mock import Mock

from pastepwn.util.listify import listify


class ListifyTest(unittest.TestCase):

    def test_None(self):
        self.assertEqual([], listify(None), "Listify did not return empty list!")

    def test_list(self):
        obj = Mock()
        obj2 = Mock()
        obj3 = Mock()
        obj_list = [obj, obj2, obj3]

        self.assertEqual(obj_list, listify(obj_list), "Listify did not return the given list!")

    def test_single(self):
        obj = Mock()
        self.assertEqual([obj], listify(obj), "Listify did not return single object as list!")


if __name__ == "__main__":
    unittest.main()
