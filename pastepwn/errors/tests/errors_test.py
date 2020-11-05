# -*- coding: utf-8 -*-
import unittest
from unittest.mock import Mock

from pastepwn.errors.errors import PastepwnError


class TestErrors(unittest.TestCase):
    def setUp(self):
        """
        Sets the result of this thread.

        Args:
            self: (todo): write your description
        """
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


if __name__ == '__main__':
    unittest.main()
