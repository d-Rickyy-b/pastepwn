# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from pastepwn.analyzers.shahashanalyzer import SHAHashAnalyzer


class TestSHAHashAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = SHAHashAnalyzer(None)
        self.paste = mock.Mock()

    def test_match_positive(self):
        """Test if positives are recognized"""
        # obtained by: $ echo "foo" | shasum
        self.paste.body = "f1d2d2f924e986ac86fdf7b36c94bcdf32beec15"
        self.assertTrue(self.analyzer.match(self.paste))

        # obtained by: $ echo "foo" | shasum -a 224
        self.paste.body = "e7d5e36e8d470c3e5103fedd2e4f2aa5c30ab27f6629bdc3286f9dd2"
        self.assertTrue(self.analyzer.match(self.paste))

        # obtained by: $ echo "foo" | shasum -a 256
        self.paste.body = "b5bb9d8014a0f9b1d61e21e796d78dccdf1352f23cd32812f4850b878ae4944c"
        self.assertTrue(self.analyzer.match(self.paste))

        # obtained by: $ echo "foo" | shasum -a 384
        self.paste.body = "8effdabfe14416214a250f935505250bd991f106065d899db6e19bdc8bf648f3ac0f1935c4f65fe8f798289b1a0d1e06"
        self.assertTrue(self.analyzer.match(self.paste))

        # obtained by: $ echo "foo" | shasum -a 512
        self.paste.body = "0cf9180a764aba863a67b6d72f0918bc131c6772642cb2dce5a34f0a702f9470ddc2bf125c12198b1995c233c34b4afd346c54a2334c350a948a51b6e8b4e6b6"
        self.assertTrue(self.analyzer.match(self.paste))

        self.paste.body = "my super cool hash is f1d2d2f924e986ac86fdf7b36c94bcdf32beec15 and here's some more text"
        self.assertTrue(self.analyzer.match(self.paste))

        # Newline-separated valid hashes
        self.paste.body = "f1d2d2f924e986ac86fdf7b36c94bcdf32beec15\ne7d5e36e8d470c3e5103fedd2e4f2aa5c30ab27f6629bdc3286f9dd2"
        self.assertTrue(self.analyzer.match(self.paste))

    def test_match_negative(self):
        """Test if negatives are not recognized"""
        self.paste.body = ""
        self.assertFalse(self.analyzer.match(self.paste))

        self.paste.body = None
        self.assertFalse(self.analyzer.match(self.paste))

        # Invalid character 'g'
        self.paste.body = "1234567890abcdefg"
        self.assertFalse(self.analyzer.match(self.paste))

        # MD5 Hash
        self.paste.body = "9e107d9d372bb6826bd81d3542a419d6"
        self.assertFalse(self.analyzer.match(self.paste))

        # Invalid SHA hash length
        self.paste.body = 41 * "a"
        self.assertFalse(self.analyzer.match(self.paste))
        self.paste.body = 513 * "a"
        self.assertFalse(self.analyzer.match(self.paste))


if __name__ == "__main__":
    unittest.main()
