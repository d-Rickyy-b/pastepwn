# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from pastepwn.analyzers.slacktokenanalyzer import SlackTokenAnalyzer


class TestSlackTokenAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = SlackTokenAnalyzer(None)
        self.paste = mock.Mock()

    def test_match_positive(self):
        """Test if positives are recognized"""
        # slack key dump
        self.paste.body = "xoxb-999999999999-999999999999-999999999999-9999999999999999999999999999999a"
        self.assertTrue(self.analyzer.match(self.paste))

        # slack key dump
        self.paste.body = "xoxb-999999999999-999999999999-999999999999-99999999999999999999999999999999"
        self.assertTrue(self.analyzer.match(self.paste))

        # slack key dump
        self.paste.body = "xoxp-999999999999-999999999999-999999999999-99999999999999999999999999999999"
        self.assertTrue(self.analyzer.match(self.paste))

        # slack key dump
        self.paste.body = "xoxa-999999999999-999999999999-999999999999-99999999999999999999999999999999"
        self.assertTrue(self.analyzer.match(self.paste))

        # sentance segment slack key
        self.paste.body = "my token is: xoxo-999999999999-999999999999-999999999999-99999999999999abc999999999999999"
        self.assertTrue(self.analyzer.match(self.paste))

    def test_match_negative(self):
        """Test if negatives are not recognized"""
        self.paste.body = ""
        self.assertFalse(self.analyzer.match(self.paste))

        self.paste.body = 'my bike isn\'t a number'
        self.assertFalse(self.analyzer.match(self.paste))

        # Invalid length
        self.paste.body = "xoxa-999999999999-999999999999-99999999999-99999999999999999999999999999999"
        self.assertFalse(self.analyzer.match(self.paste))

        # Upper-case
        self.paste.body = "my token is: xoxo-999999999999-999999999999-999999999999-99999999999999Abc999999999999999"
        self.assertFalse(self.analyzer.match(self.paste))
        # too short and Upper-case
        self.paste.body = "my token is: xoxo-999999999999-999999999999-99999999999-99999999999999Abc999999999999999"
        self.assertFalse(self.analyzer.match(self.paste))


if __name__ == '__main__':
    unittest.main()
