# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from pastepwn.analyzers.pastebinurlanalyzer import PastebinURLAnalyzer


class TestPastebinURLAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = PastebinURLAnalyzer(None)
        self.paste = mock.Mock()

    def test_match_positive(self):
        self.paste.body = "https://pastebin.com/xyz"
        self.assertTrue(self.analyzer.match(self.paste))
        self.paste.body = "https://pastebin.com/xyz/"
        self.assertTrue(self.analyzer.match(self.paste))
        self.paste.body = "http://pastebin.com/xyz"
        self.assertTrue(self.analyzer.match(self.paste))
        self.paste.body = "http://pastebin.com/xyz/"
        self.assertTrue(self.analyzer.match(self.paste))
        self.paste.body = "https://pastebin.com/xyz  "
        self.assertTrue(self.analyzer.match(self.paste))
        self.paste.body = "www.pastebin.com/xyz"
        self.assertTrue(self.analyzer.match(self.paste))
        self.paste.body = "pastebin.com/xyx"
        self.assertTrue(self.analyzer.match(self.paste))
        self.paste.body = "This is a pastebin URL: pastebin.com/ya249asd - and this is a test"

    def test_match_negative(self):
        self.paste.body = ""
        self.assertFalse(self.analyzer.match(self.paste))
        self.paste.body = None
        self.assertFalse(self.analyzer.match(self.paste))
        self.paste.body = "https://google.com/xyz"
        self.assertFalse(self.analyzer.match(self.paste))
        self.paste.body = "xyzpastebin.com/k"
        self.assertFalse(self.analyzer.match(self.paste))
        self.paste.body = "https://pastebin.com/"
        self.assertFalse(self.analyzer.match(self.paste))

    if __name__ == "__main__":
        unittest.main()
