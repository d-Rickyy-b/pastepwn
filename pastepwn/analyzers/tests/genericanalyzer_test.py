# -*- coding: utf-8 -*-
import unittest
from unittest.mock import Mock, MagicMock

from pastepwn.actions.basicaction import BasicAction
from pastepwn.analyzers import GenericAnalyzer


class TestGenericAnalyzer(unittest.TestCase):
    def setUp(self):
        self.mock_action = MagicMock(spec=BasicAction)

    def test_empty_match_func(self):
        """Check if a ValueError rises on empty match_func"""
        with self.assertRaises(ValueError, msg="No exception was raised although the match_func is None"):
            GenericAnalyzer(self.mock_action, None)

    def test_not_callable_match_func(self):
        """Check if ValueError rises on anything but a callable"""
        test_int = 1
        with self.assertRaises(ValueError, msg="No exception was raised although the match_func is not callable"):
            GenericAnalyzer(self.mock_action, test_int)

        test_string = "Test"
        with self.assertRaises(ValueError, msg="No exception was raised although the match_func is not callable"):
            GenericAnalyzer(self.mock_action, test_string)

    def test_perform(self):
        """Test to check if a given match_func will be executed when calling match()"""
        mock_func = Mock(return_value=True)
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
        self.assertTrue(mock_exception.call_count > 0, msg="The mock has not been called!")

        # Make sure the analyzer returned false as result
        self.assertFalse(result, msg="The analyzer returned true although an exception was raised!")

    def test_empty_verify_func(self):
        """Test if passing None as verify function works out fine"""
        mock_func = Mock()
        ga = GenericAnalyzer(self.mock_action, mock_func, None)
        self.assertEqual(ga.verify_func, None)

    def test_not_callable_verify_func(self):
        """Check if ValueError rises on anything but a callable as verify_method (apart from None)"""
        mock_func = Mock()
        non_callable_obj = "This is a string, not a function you idiot!"
        with self.assertRaises(ValueError, msg="No exception was raised although the verify_func is not callable"):
            _ = GenericAnalyzer(self.mock_action, mock_func, non_callable_obj)

    def test_verify(self):
        """Test to check if a given verify_func will be executed when calling match()"""
        mock_match_func = Mock(return_value=True)
        mock_verify_func = Mock(return_value=True)
        mock_paste = Mock()

        ga = GenericAnalyzer(self.mock_action, match_func=mock_match_func, verify_func=mock_verify_func)
        ga.match(paste=mock_paste)
        mock_match_func.assert_called_with(mock_paste)

    def test_verify_negative(self):
        """Test to check if match() function returns False if verify retruns False"""
        match_ret_val = ["match1", "match2"]
        mock_match_func = Mock(return_value=match_ret_val)
        mock_verify_func = Mock(return_value=False)
        mock_paste = Mock()

        ga = GenericAnalyzer(self.mock_action, match_func=mock_match_func, verify_func=mock_verify_func)
        res = ga.match(paste=mock_paste)
        self.assertFalse(res, "The analyzer matched, although it shouldn't")
        mock_verify_func.assert_called_with(match_ret_val)

    def test_verify_exception(self):
        """Test to check if the analyzer will catch and log exceptions from the verify_func"""
        mock_match_func = Mock(return_value=True)
        mock_verify_exception = Mock(side_effect=ValueError)
        mock_verify_exception.__name__ = "mock_match_exception"
        mock_paste = Mock()

        # Initialize analyzer and execute match function
        ga = GenericAnalyzer(self.mock_action, match_func=mock_match_func, verify_func=mock_verify_exception)
        result = ga.match(mock_paste)

        # Make sure the verify method was called
        self.assertTrue(mock_verify_exception.call_count > 0, msg="The mock has not been called!")

        # Make sure the analyzer returned false as result
        self.assertFalse(result, msg="The analyzer returned true although an exception was raised!")


if __name__ == "__main__":
    unittest.main()
