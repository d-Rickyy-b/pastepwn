# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from pastepwn.analyzers.awsaccesskeyanalyzer import AWSAccessKeyAnalyzer


class TestAWSAccessKeyAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = AWSAccessKeyAnalyzer(None)
        self.paste = mock.Mock()

    def test_match_positive(self):
        """Test if positives are recognized"""
        # obtained by pastebin search
        self.paste.body = "AKIAIX2GUZJMJFDZON4A"
        self.assertTrue(self.analyzer.match(self.paste))

        # obtained by pastebin search
        self.paste.body = "AKIAJ5OVIVTO7XQ7UWOQ"
        self.assertTrue(self.analyzer.match(self.paste))

        # obtained by pastebin search
        self.paste.body = "AKIAJM4DOPAAJWLUJ2PQ"
        self.assertTrue(self.analyzer.match(self.paste))

        # obtained by pastebin search
        self.paste.body = "AKIAIKSA47YZNJAY2H6A"
        self.assertTrue(self.analyzer.match(self.paste))

    def test_match_intext(self):
        self.paste.body = "my super cool hash is AKIAJM4DOPAAJWLUJ2PQ and here's some more text"
        match = self.analyzer.match(self.paste)
        self.assertTrue(match)
        self.assertEqual("AKIAJM4DOPAAJWLUJ2PQ", match[0])

        self.paste.body = "AWS Access Key ID [None]: AKIAIX2GUZJMJFDZON4A"
        match = self.analyzer.match(self.paste)
        self.assertTrue(match)
        self.assertEqual("AKIAIX2GUZJMJFDZON4A", match[0])

    def test_multiple(self):
        # Newline-separated valid hashes
        self.paste.body = "AKIAIKSA47YZNJAY2H6A\nAKIAJM4DOPAAJWLUJ2PQ"
        self.assertTrue(self.analyzer.match(self.paste))
        match = self.analyzer.match(self.paste)
        self.assertTrue(match)
        self.assertEqual("AKIAIKSA47YZNJAY2H6A", match[0])
        self.assertEqual("AKIAJM4DOPAAJWLUJ2PQ", match[1])

    def test_match_negative(self):
        """Test if negatives are not recognized"""
        self.paste.body = ""
        self.assertFalse(self.analyzer.match(self.paste))

        self.paste.body = None
        self.assertFalse(self.analyzer.match(self.paste))

        # Invalid character '-'
        self.paste.body = "AKIAIX2GUZJMJFD-ON4A"
        self.assertFalse(self.analyzer.match(self.paste))

        # Different prefix
        self.paste.body = "AKIBIX2GUZJMJFDZON4A"
        self.assertFalse(self.analyzer.match(self.paste))

        # Invalid length
        self.paste.body = "AKIAIX2GUZJMJFDZON4"
        self.assertFalse(self.analyzer.match(self.paste))
        self.paste.body = "AKIAIX2GUZJMJFDZON4AA"
        self.assertFalse(self.analyzer.match(self.paste))


if __name__ == "__main__":
    unittest.main()
