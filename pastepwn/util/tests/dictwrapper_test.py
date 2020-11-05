# -*- coding: utf-8 -*-
import unittest

from pastepwn.util.dictwrapper import DictWrapper


class TestDictwrapper(unittest.TestCase):
    def setUp(self):
        """
        Set the test ::

        Args:
            self: (todo): write your description
        """
        self.test_dict = {"key1": "value1", "key2": "value2"}

    def test_existing_key(self):
        """
        The test key exists in the test.

        Args:
            self: (todo): write your description
        """
        test_wrapped = DictWrapper(self.test_dict)
        self.assertEqual(test_wrapped["key1"], "value1")

    def test_non_existing_key(self):
        """
        This function that the test key of the given test.

        Args:
            self: (todo): write your description
        """
        test_wrapped = DictWrapper(self.test_dict)
        # Make sure that retreiving a valid key works
        self.assertEqual(test_wrapped["key1"], "value1")
        # Check if retreiving a nonexistent value works as expected
        self.assertEqual(test_wrapped["key3"], "${key3}")
        # Make sure that retreiving a valid key still works
        self.assertEqual(test_wrapped["key2"], "value2")


if __name__ == '__main__':
    unittest.main()
