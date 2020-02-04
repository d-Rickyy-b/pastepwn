# -*- coding: utf-8 -*-
import unittest
from unittest import mock

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
        analyzer = AlwaysTrueAnalyzer(self.paste)
        self.assertEqual([self.paste], analyzer.actions)


if __name__ == '__main__':
    unittest.main()
