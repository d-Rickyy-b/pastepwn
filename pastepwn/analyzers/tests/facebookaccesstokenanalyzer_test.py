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

    def test_intext(self):
        """Test if matches inside text are recognized"""
        self.obj.body = "This is my access token: EAACEdEose0cBA0123456789ABCDEFabcdef, please don't lose it!"
        match = self.analyzer.match(self.obj)
        self.assertTrue(match)
        self.assertEqual("EAACEdEose0cBA0123456789ABCDEFabcdef", match[0])

    def test_multiple(self):
        """Test if multiple matches are recognized"""
        self.obj.body = "This is my access token: EAACEdEose0cBA0123456789ABCDEFabcdef, please don't lose it! " \
                        "Also there is another one: EAACEdEose0cBAfacebooksucks so I guess it's ok"
        match = self.analyzer.match(self.obj)
        self.assertTrue(match)
        self.assertEqual("EAACEdEose0cBA0123456789ABCDEFabcdef", match[0])
        self.assertEqual("EAACEdEose0cBAfacebooksucks", match[1])

    def test_match_positive(self):
        # random valid string
        self.obj.body = "EAACEdEose0cBA0123456789ABCDEFabcdef"
        self.assertTrue(self.analyzer.match(self.obj))


if __name__ == '__main__':
    unittest.main()
