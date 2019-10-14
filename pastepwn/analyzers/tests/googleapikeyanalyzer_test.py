# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from pastepwn.analyzers.googleapikeyanalyzer import GoogleApiKeyAnalyzer


class TestGoogleApiKeyAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = GoogleApiKeyAnalyzer(None)
        self.paste = mock.Mock()

    def test_match_positive(self):
        """Test if positives are recognized"""
        # google key dump
        self.paste.body = "AIzaSyCTmst6SvsOAQanZKNt-2pt6nuLoFf2kSA"
        self.assertTrue(self.analyzer.match(self.paste))

        # google key dump
        self.paste.body = "AIzaSyBKNst9JE89f4lHuNXQFTUgZKh8VZpvR6M"
        self.assertTrue(self.analyzer.match(self.paste))

        # google key dump
        self.paste.body = "AIzammmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm"
        self.assertTrue(self.analyzer.match(self.paste))

        # google key dump
        self.paste.body = "AIza00000000000000000000000000000000000"
        self.assertTrue(self.analyzer.match(self.paste))

    def test_match_negative(self):
        """Test if negatives are not recognized"""
        self.paste.body = ""
        self.assertFalse(self.analyzer.match(self.paste))

        self.paste.body = None
        self.assertFalse(self.analyzer.match(self.paste))

        # Invalid start
        self.paste.body = "aiza00000000000000000000000000000000000"
        self.assertFalse(self.analyzer.match(self.paste))

        # Invalid start
        self.paste.body = "000000000000000000000000000000000000000"
        self.assertFalse(self.analyzer.match(self.paste))

        # Invalid length
        self.paste.body = "AIzammmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm"
        self.assertFalse(self.analyzer.match(self.paste))

        # Invalid length
        self.paste.body = "AIzammmmmmmmm"
        self.assertFalse(self.analyzer.match(self.paste))

if __name__ == '__main__':
    unittest.main()
