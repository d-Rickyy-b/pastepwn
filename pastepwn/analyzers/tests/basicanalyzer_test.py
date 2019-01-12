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
        actions = mock.Mock()
        analyzer = BasicAnalyzer(actions)
        self.assertEqual([actions], analyzer.actions)

    def test_empty_initialization(self):
        analyzer = BasicAnalyzer(None)
        self.assertEqual([], analyzer.actions)

    def test_single_initialization(self):
        analyzer = BasicAnalyzer(self.obj)
        self.assertEqual([self.obj], analyzer.actions)

    def test_multi_initialization(self):
        obj2 = mock.Mock()
        actions = [self.obj, obj2]
        analyzer = BasicAnalyzer(actions)
        self.assertEqual([self.obj, obj2], analyzer.actions)


if __name__ == '__main__':
    unittest.main()
