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

    def test_intext(self):
        """Test if matches inside text are recognized"""
        # key appearing in the middle of a string
        self.paste.body = "my azure key is: a32324343543bcdea32324343543bcde, aaaa"
        match = self.analyzer.match(self.paste)
        self.assertTrue(match)
        self.assertEqual("a32324343543bcdea32324343543bcde", match[0])

    def test_multiple(self):
        """Test if multiple matches are recognized"""
        self.paste.body = "There are multiple keys: a32324343543bcdea32324343543bcde, " \
                          "aaaand also aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa!"
        match = self.analyzer.match(self.paste)
        self.assertTrue(match)
        self.assertEqual("a32324343543bcdea32324343543bcde", match[0])
        self.assertEqual("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", match[1])

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


if __name__ == "__main__":
    unittest.main()
