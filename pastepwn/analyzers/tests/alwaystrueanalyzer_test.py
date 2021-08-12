# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from pastepwn.actions.basicaction import BasicAction
from pastepwn.analyzers.alwaystrueanalyzer import AlwaysTrueAnalyzer


class TestAlwaysTrueAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = AlwaysTrueAnalyzer(None)
        self.paste = mock.Mock()

    def test_match(self):
        self.paste.body = "Test"
        self.assertTrue(self.analyzer.match(self.paste))

        self.paste.body = None
        self.assertTrue(self.analyzer.match(self.paste))

        self.paste.body = ""
        self.assertTrue(self.analyzer.match(self.paste))

        self.paste = None
        self.assertTrue(self.analyzer.match(self.paste))

    def test_actions_present(self):
        action = mock.MagicMock(spec=BasicAction)
        analyzer = AlwaysTrueAnalyzer(action)
        self.assertEqual([action], analyzer.actions)


if __name__ == "__main__":
    unittest.main()
