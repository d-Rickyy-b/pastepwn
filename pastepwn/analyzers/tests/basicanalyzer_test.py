# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from pastepwn.analyzers.basicanalyzer import BasicAnalyzer


class TestBasicAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = BasicAnalyzer(None)
        self.mock_action = mock.Mock()

    def test_add_action(self):
        """Check if it's possible to add actions to an analyzer"""
        mock_action2 = mock.Mock
        analyzer = BasicAnalyzer(self.mock_action)
        self.assertEqual([self.mock_action], analyzer.actions)

        analyzer.add_action(mock_action2)
        self.assertTrue(isinstance(analyzer.actions, list))
        self.assertEqual([self.mock_action, mock_action2], analyzer.actions)

    def test_match(self):
        """Check if an exception is raised when trying to call the match function"""
        self.mock_action.body = "Test"
        self.assertRaises(NotImplementedError, self.analyzer.match, self.mock_action)

    def test_initialization(self):
        """Check if the initialization of the BasicAnalyzer works as intended"""
        actions = mock.Mock()
        analyzer = BasicAnalyzer(actions)
        self.assertEqual([actions], analyzer.actions)

    def test_empty_initialization(self):
        analyzer = BasicAnalyzer(None)
        self.assertEqual([], analyzer.actions)

    def test_single_initialization(self):
        analyzer = BasicAnalyzer(self.mock_action)
        self.assertEqual([self.mock_action], analyzer.actions)

    def test_multi_initialization(self):
        mock_action2 = mock.Mock()
        actions = [self.mock_action, mock_action2]
        analyzer = BasicAnalyzer(actions)
        self.assertEqual([self.mock_action, mock_action2], analyzer.actions)


if __name__ == '__main__':
    unittest.main()
