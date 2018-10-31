# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from pastepwn.analyzers.alwaystrueanalyzer import AlwaysTrueAnalyzer


class TestAlwaysTrueAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = AlwaysTrueAnalyzer(None)
        self.obj = mock.Mock()

    def test_match(self):
        self.obj.body = "Test"
        self.assertTrue(self.analyzer.match(self.obj))

        self.obj.body = None
        self.assertTrue(self.analyzer.match(self.obj))

        self.obj.body = ""
        self.assertTrue(self.analyzer.match(self.obj))

        self.obj = None
        self.assertTrue(self.analyzer.match(self.obj))


if __name__ == '__main__':
    unittest.main()
