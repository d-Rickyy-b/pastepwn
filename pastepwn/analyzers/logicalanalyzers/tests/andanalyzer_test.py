# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from pastepwn.analyzers import AndAnalyzer


class TestAndAnalyzer(unittest.TestCase):
    def setUp(self):
        self.obj = mock.Mock()
        self.gt = mock.Mock()
        self.gt.match = mock.Mock(return_value=True)

        self.gf = mock.Mock()
        self.gf.match = mock.Mock(return_value=False)

    def test_match_positive(self):
        self.obj.body = "Test"
        analyzer = AndAnalyzer(None, [self.gt])
        self.assertTrue(analyzer.match(self.obj))

        analyzer = AndAnalyzer(None, [self.gt, self.gt, self.gt])
        self.assertTrue(analyzer.match(self.obj))

        # Check if the analyzer returns false if there is at least one false result
        analyzer = AndAnalyzer([], [self.gt, self.gf])
        self.assertFalse(analyzer.match(self.obj))

        analyzer = AndAnalyzer([], [self.gf, self.gf])
        self.assertFalse(analyzer.match(self.obj))

        analyzer = AndAnalyzer([], [self.gf, self.gf, self.gf, self.gt])
        self.assertFalse(analyzer.match(self.obj))

    def test_negative(self):
        self.obj.body = ""

        analyzer = AndAnalyzer([], None)
        self.assertFalse(analyzer.match(self.obj))

        analyzer = AndAnalyzer([], [])
        self.assertFalse(analyzer.match(self.obj))

    def test_actions_present(self):
        analyzer = AndAnalyzer(self.obj, None)
        self.assertEqual([self.obj], analyzer.actions)

    def test_analyzers_present(self):
        analyzer = AndAnalyzer(None, self.obj)
        self.assertEqual([self.obj], analyzer.analyzers)


if __name__ == '__main__':
    unittest.main()
