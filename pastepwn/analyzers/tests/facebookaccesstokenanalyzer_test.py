# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from pastepwn.analyzers.facebookaccesstokenanalyzer import FacebookAccessTokenAnalyzer


class TestFacebookAccessTokenAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = FacebookAccessTokenAnalyzer(None)
        self.obj = mock.Mock()

    def test_match_negative(self):
        # random string
        self.obj.body = "Test"
        self.assertFalse(self.analyzer.match(self.obj))

        # empty
        self.obj.body = ""
        self.assertFalse(self.analyzer.match(self.obj))

        # non-alphanumeric
        self.obj.body = "EAACEdEose0cBA!abcdef"
        self.assertFalse(self.analyzer.match(self.obj))

        # invalid prefix
        self.obj.body = "EAAACEdEose0cBAabcdef"
        self.assertFalse(self.analyzer.match(self.obj))

        # invalid params
        self.obj.body = None
        self.assertFalse(self.analyzer.match(self.obj))

        self.obj = None
        self.assertFalse(self.analyzer.match(self.obj))

    def test_match_negative(self):
        # random string
        self.obj.body = "Test"
        self.assertFalse(self.analyzer.match(self.obj))

        # empty
        self.obj.body = ""
        self.assertFalse(self.analyzer.match(self.obj))

        # non-alphanumeric
        self.obj.body = "EAACEdEose0cBA!abcdef"
        self.assertFalse(self.analyzer.match(self.obj))

        # invalid prefix
        self.obj.body = "EAAACEdEose0cBAabcdef"
        self.assertFalse(self.analyzer.match(self.obj))

        # invalid params
        self.obj.body = None
        self.assertFalse(self.analyzer.match(self.obj))

        self.obj = None
        self.assertFalse(self.analyzer.match(self.obj))

    def test_match_positive(self):
        # random valid string
        self.obj.body = "EAACEdEose0cBA0123456789ABCDEFabcdef"
        self.assertTrue(self.analyzer.match(self.obj))


if __name__ == '__main__':
    unittest.main()
