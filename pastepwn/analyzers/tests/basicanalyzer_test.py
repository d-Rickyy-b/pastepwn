# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from pastepwn.analyzers.basicanalyzer import BasicAnalyzer


class TestBasicAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = BasicAnalyzer(None)
        self.obj = mock.Mock()

    def test_match(self):
        """Check if an exception is raised when trying to call the match function"""
        self.obj.body = "Test"
        self.assertRaises(NotImplementedError, self.analyzer.match, self.obj)

    def test_initialization(self):
        """Check if the initialization of the BasicAnalyzer works as intended"""
        action = mock.Mock()
        analyzer = BasicAnalyzer(action)
        self.assertEqual(action, analyzer.action)


if __name__ == '__main__':
    unittest.main()
