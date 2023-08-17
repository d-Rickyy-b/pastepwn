# -*- coding: utf-8 -*-
import unittest
from unittest.mock import Mock

from pastepwn.errors.errors import PastepwnError


class TestErrors(unittest.TestCase):
    def setUp(self):
        pass

    def test_PastepwnError(self):
        """Test if the PastepwnError returns its string message"""
        msg = "This is a test message"
        error = PastepwnError(msg)
        self.assertEqual(msg, error.message)
        self.assertEqual(msg, str(error))

        mock = Mock()
        mock.__str__ = Mock(return_value="This is just another test message")
        error = PastepwnError(mock)
        self.assertEqual(mock, error.message)
        self.assertEqual(str(mock), str(error))

    def test_PastepwnError_with_empty_message(self):
        """Test if the PastepwnError handles an empty message"""
        empty_msg = ""
        error = PastepwnError(empty_msg)
        self.assertEqual(empty_msg, error.message)
        self.assertEqual(empty_msg, str(error))

    def test_PastepwnError_with_none_message(self):
        """Test if the PastepwnError handles a None message"""
        error = PastepwnError(None)
        self.assertIsNone(error.message)
        self.assertEqual("None", str(error))

    def test_PastepwnError_with_custom_object(self):
        """Test if the PastepwnError handles a custom object message"""
        custom_obj = {"key": "value"}
        error = PastepwnError(custom_obj)
        self.assertEqual(custom_obj, error.message)
        self.assertEqual(str(custom_obj), str(error))

    def test_PastepwnError_with_unicode_message(self):
        """Test if the PastepwnError handles a Unicode message"""
        unicode_msg = "Unicode ➔ ✓"
        error = PastepwnError(unicode_msg)
        self.assertEqual(unicode_msg, error.message)
        self.assertEqual(unicode_msg, str(error))


if __name__ == "__main__":
    unittest.main()
