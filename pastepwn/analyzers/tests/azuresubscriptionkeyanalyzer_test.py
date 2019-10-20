# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from pastepwn.analyzers.azuresubscriptionkeyanalyzer import AzureSubscriptionKeyAnalyzer


class TestAzureSubscriptionKeyAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = AzureSubscriptionKeyAnalyzer(None)
        self.paste = mock.Mock()

    def test_match_positive(self):
        """Test if positives are recognized"""
        # google key dump
        self.paste.body = "74796abfc83c49bba7458746266abd28"
        self.assertTrue(self.analyzer.match(self.paste))

        # google key dump
        self.paste.body = "00000000000000000000000000000000"
        self.assertTrue(self.analyzer.match(self.paste))

        # google key dump
        self.paste.body = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        self.assertTrue(self.analyzer.match(self.paste))

        # google key dump
        self.paste.body = "a32324343543bcdea32324343543bcde"
        self.assertTrue(self.analyzer.match(self.paste))

        # key appearing in the middle of a string
        self.paste.body = "my azure key is: a32324343543bcdea32324343543bcde, aaaa"
        self.assertTrue(self.analyzer.match(self.paste))

    def test_match_negative(self):
        """Test if negatives are not recognized"""
        self.paste.body = ""
        self.assertFalse(self.analyzer.match(self.paste))

        self.paste.body = None
        self.assertFalse(self.analyzer.match(self.paste))

        # Invalid characters
        self.paste.body = "aaaaaaaaaaaaaaa-aaaaaaaaaaaaaaaa"
        self.assertFalse(self.analyzer.match(self.paste))

        # Invalid casing
        self.paste.body = "AAAAAAAABBBB11111111111111111111"
        self.assertFalse(self.analyzer.match(self.paste))

        # Invalid length
        self.paste.body = "AAAAAAAAAA"
        self.assertFalse(self.analyzer.match(self.paste))

        # Invalid length
        self.paste.body = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        self.assertFalse(self.analyzer.match(self.paste))

if __name__ == '__main__':
    unittest.main()
