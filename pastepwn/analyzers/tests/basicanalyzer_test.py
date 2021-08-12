# -*- coding: utf-8 -*-
import logging
import unittest
from unittest import mock

from pastepwn.actions.basicaction import BasicAction
from pastepwn.analyzers.basicanalyzer import BasicAnalyzer
from pastepwn.errors import InvalidActionError


class TestBasicAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = BasicAnalyzer(None)
        self.mock_action = mock.MagicMock(spec=BasicAction)

    def test_add_action(self):
        """Check if it's possible to add actions to an analyzer"""
        mock_action2 = mock.MagicMock(spec=BasicAction)
        analyzer = BasicAnalyzer(self.mock_action)
        self.assertEqual([self.mock_action], analyzer.actions)

        analyzer.add_action(mock_action2)
        self.assertIsInstance(analyzer.actions, list)
        self.assertEqual([self.mock_action, mock_action2], analyzer.actions)

    def test_add_action_negative(self):
        """Check if an exception raises when passing crap as action"""
        analyzer = BasicAnalyzer(self.mock_action)
        self.assertEqual([self.mock_action], analyzer.actions)

        with self.assertRaises(InvalidActionError, msg="BasicAnalyzer accepts objects other than BasicAnalyzers as actions in add_action!"):
            # The mock_action2 is not a subclass of BasicAction and hence it must throw an error
            mock_action2 = mock.Mock()
            analyzer.add_action(mock_action2)

        with self.assertRaises(InvalidActionError, msg="BasicAnalyzer accepts classes as actions in add_action!"):
            # The mock_action3 is not even an object (only a class reference)
            mock_action3 = mock.Mock
            analyzer.add_action(mock_action3)

    def test_match(self):
        """Check if an exception is raised when trying to call the match function"""
        self.mock_action.body = "Test"
        self.assertRaises(NotImplementedError, self.analyzer.match, self.mock_action)

    def test_initialization(self):
        """Check if the initialization of the BasicAnalyzer works as intended"""
        analyzer = BasicAnalyzer(self.mock_action)
        self.assertEqual([self.mock_action], analyzer.actions)

    def test_empty_initialization(self):
        """Check if initializing an analyzer without actions is possible"""
        analyzer = BasicAnalyzer(None)
        self.assertEqual([], analyzer.actions)

    def test_single_initialization(self):
        """Check if initializing an analyzer with a single action is possible"""
        analyzer = BasicAnalyzer(self.mock_action)
        self.assertEqual([self.mock_action], analyzer.actions)

    def test_multi_initialization(self):
        """Check if initializing an analyzer with multiple actions is possible"""
        mock_action2 = mock.MagicMock(spec=BasicAction)
        actions = [self.mock_action, mock_action2]
        analyzer = BasicAnalyzer(actions)
        self.assertEqual([self.mock_action, mock_action2], analyzer.actions)

    def test_logical_operators(self):
        """Check if using logical operators on analyzers works as intended"""
        analyzer = self.analyzer & self.analyzer
        self.assertIsInstance(analyzer, BasicAnalyzer)

        mock_action1 = mock.MagicMock(spec=BasicAction)
        mock_action2 = mock.MagicMock(spec=BasicAction)
        analyzer1 = BasicAnalyzer(mock_action1)
        analyzer2 = BasicAnalyzer(mock_action2)

        and_analyzer = analyzer1 & analyzer2
        self.assertEqual(2, len(and_analyzer.actions))
        self.assertIn(mock_action1, and_analyzer.actions)
        self.assertIn(mock_action2, and_analyzer.actions)
        self.assertEqual("(BasicAnalyzer && BasicAnalyzer)", and_analyzer.identifier)

    def test_init_action_class(self):
        """Check if an exception is being raised when a passed action is a reference to a class"""
        # Test created based on #175
        # If users pass a class instead of an instance, they should receive an exception
        with self.assertRaises(InvalidActionError, msg="BasicAnalyzer accepts classes as actions!"):
            _ = BasicAnalyzer(mock.Mock)

    def test_error_logging_init_class(self):
        """Check if an error is being logged when a passed action is a reference to a class"""
        self.logger = logging.getLogger("pastepwn.analyzers.basicanalyzer")
        with self.assertLogs(self.logger, level="ERROR") as log:
            try:
                _ = BasicAnalyzer(mock.Mock)
            except Exception:
                pass

            self.assertEqual(log.output, ["ERROR:pastepwn.analyzers.basicanalyzer:You passed a class as action for 'BasicAnalyzer' but an instance of an action was expected!"])

    def test_unique(self):
        """Check if running unique() on a list of matches returns a list with no duplicates."""
        # Some lists with and without duplicates
        test_lists = [
            [],
            ["a", "a"],
            ["a", "b"],
            ["a", "b", "a"]
            ]
        self.assertEqual(BasicAnalyzer.unique(test_lists[0]), [],
                         msg="BasicAnalyzer.unique() left a duplicate!")
        self.assertEqual(BasicAnalyzer.unique(test_lists[1]), ["a"],
                         msg="BasicAnalyzer.unique() left a duplicate!")
        # Should preserve order
        self.assertEqual(BasicAnalyzer.unique(test_lists[2]), ["a", "b"],
                         msg="BasicAnalyzer.unique() left a duplicate!")
        self.assertEqual(BasicAnalyzer.unique(test_lists[3]), ["a", "b"],
                         msg="BasicAnalyzer.unique() left a duplicate!")


if __name__ == "__main__":
    unittest.main()
