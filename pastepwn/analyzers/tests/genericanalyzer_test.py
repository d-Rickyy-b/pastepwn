# -*- coding: utf-8 -*-
import unittest
from unittest.mock import Mock

from pastepwn.analyzers import GenericAnalyzer


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.mock_action = Mock()

    def test_empty_match_func(self):
        # Check if a ValueError rises on empty match_func
        with self.assertRaises(ValueError, msg="No exception was raised although the match_func is None"):
            GenericAnalyzer(self.mock_action, None)

    def test_not_callable_match_func(self):
        # Check if ValueError rises on anything but a callable
        test_int = 1
        with self.assertRaises(ValueError, msg="No exception was raised although the match_func is not callable"):
            GenericAnalyzer(self.mock_action, test_int)

        test_string = "Test"
        with self.assertRaises(ValueError, msg="No exception was raised although the match_func is not callable"):
            GenericAnalyzer(self.mock_action, test_string)

    def test_perform(self):
        """Test to check if a given action will be executed when the analyzer function returns True"""
        mock_func = Mock()
        mock_func.perform = Mock(return_value=True)
        mock_paste = Mock()

        ga = GenericAnalyzer(self.mock_action, mock_func)
        ga.match(paste=mock_paste)
        mock_func.assert_called_with(mock_paste)

    def test_perform_exception(self):
        """Test to check if the analyzer will catch and log exceptions from the match_func"""
        mock_exception = Mock(side_effect=ValueError)
        mock_exception.__name__ = "mock_match_exception"
        mock_paste = Mock()

        # Initialize analyzer and execute match function
        ga = GenericAnalyzer(self.mock_action, mock_exception)
        result = ga.match(mock_paste)

        # Make sure the analyzer method was called
        mock_exception.assert_called_once()

        # Make sure the analyzer returned false as result
        self.assertFalse(result, msg="The analyzer returned true although an exception was raised!")


if __name__ == '__main__':
    unittest.main()
