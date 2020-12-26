# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from pastepwn.actions.basicaction import BasicAction
from pastepwn.analyzers.logicalanalyzers import LogicalBaseAnalyzer


class TestLogicalBaseAnalyzer(unittest.TestCase):
    def setUp(self):
        self.paste = mock.Mock()

    def test_exception(self):
        analyzer = LogicalBaseAnalyzer([], [])
        self.assertRaises(NotImplementedError, analyzer.match, mock.Mock())

    def test_actions_present(self):
        action = mock.MagicMock(spec=BasicAction)
        analyzer = LogicalBaseAnalyzer(action, None)
        self.assertEqual([action], analyzer.actions)

    def test_analyzers_present(self):
        analyzer = LogicalBaseAnalyzer(None, self.paste)
        self.assertEqual([self.paste], analyzer.analyzers)

    def test_merge_actions(self):
        action1 = mock.Mock()
        action2 = mock.Mock()
        action3 = mock.Mock()

        analyzer1 = mock.Mock()
        analyzer1.actions = [action1, action2]
        analyzer2 = mock.Mock()
        analyzer2.actions = [action3]

        analyzer = LogicalBaseAnalyzer(analyzers=[analyzer1, analyzer2], actions=[], merge_actions=True)
        self.assertEqual(3, len(analyzer.actions), "Wrong amount of actions in LogicalBaseAnalyzer!")
        self.assertEqual([action1, action2, action3], analyzer.actions, "Actions do not match!")


if __name__ == "__main__":
    unittest.main()
