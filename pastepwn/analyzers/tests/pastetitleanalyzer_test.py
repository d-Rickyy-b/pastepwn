# -*- coding: utf-8 -*-
import re
import unittest
from unittest import mock

from pastepwn.analyzers.pastetitleanalyzer import PasteTitleAnalyzer


class TestPasteTitleAnalyzer(unittest.TestCase):
    def setUp(self):
        """Set's up a paste mock object"""
        self.paste = mock.Mock()

    def test_matchWord(self):
        analyzer = PasteTitleAnalyzer(None, regex=r"word")
        self.paste.title = "This text contains the word 'word'!"
        self.assertTrue(analyzer.match(self.paste), "Title does not match, although it should!")

    def test_matchPattern(self):
        analyzer = PasteTitleAnalyzer(None, regex=r"\d{2}-\d{2}-\d{4}")
        self.paste.title = "This is a date 24-01-2020 inside the title"
        self.assertTrue(analyzer.match(self.paste), "Title does not match pattern!")

    def test_matchPattern2(self):
        analyzer = PasteTitleAnalyzer(None, regex=r"^The title")
        self.paste.title = "The title is cool!"
        self.assertTrue(analyzer.match(self.paste), "Title does not match pattern!")

    def test_flags(self):
        """We only test a few flags, because as long as we use regex this should work fine"""
        analyzer = PasteTitleAnalyzer(None, regex=r"ThIs iS mIxEd")
        self.paste.title = "this is mixed case (not)"
        self.assertFalse(analyzer.match(self.paste), "The regex does match, although it shouldn't!")

        # Test case independend flag / ignorecase
        analyzer = PasteTitleAnalyzer(None, regex=r"ThIs iS mIxEd", flags=re.IGNORECASE)
        self.paste.title = "this is mixed case (not)"
        self.assertTrue(analyzer.match(self.paste), "The regex does not match, although it should!")

        # Test multiline
        analyzer = PasteTitleAnalyzer(None, regex=r"^regexiscool", flags=re.MULTILINE)
        self.paste.title = "this is a multiline string\nregexiscool is right at the start of the line\nand another line!"
        self.assertTrue(analyzer.match(self.paste), "The regex does not match in multiline strings, although it should!")

    def test_emptyTitle(self):
        analyzer = PasteTitleAnalyzer(None, regex=r"Any \d pattern")
        self.paste.title = ""
        self.assertFalse(analyzer.match(self.paste), "Empty title does match pattern, although it  shouldn't!")


if __name__ == "__main__":
    unittest.main()
