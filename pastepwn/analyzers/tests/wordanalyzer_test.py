# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from pastepwn.analyzers.wordanalyzer import WordAnalyzer


class TestWordAnalyzer(unittest.TestCase):
    def setUp(self):
        self.obj = mock.Mock()

    def test_match(self):
        analyzer = WordAnalyzer(None, "Test")
        self.obj.body = "This is a Test"
        self.assertTrue(analyzer.match(self.obj))

        analyzer = WordAnalyzer(None, "Test")
        self.obj.body = "There are tests for everything"
        self.assertTrue(analyzer.match(self.obj))

        self.obj.body = "This is a Test for a longer sentence"
        self.assertTrue(analyzer.match(self.obj))

        self.obj.body = "Completely unrelated"
        self.assertFalse(analyzer.match(self.obj))

    def test_blacklist(self):
        blacklist = ["fake", "bad"]
        analyzer = WordAnalyzer(None, "Test", blacklist=blacklist)

        self.obj.body = "This is a Test"
        self.assertTrue(analyzer.match(self.obj))

        self.obj.body = "This is a fake Test"
        self.assertFalse(analyzer.match(self.obj))

        analyzer = WordAnalyzer(None, "Test", blacklist=blacklist, case_sensitive=True)

        self.obj.body = "This is a Test"
        self.assertTrue(analyzer.match(self.obj))

        self.obj.body = "This is a Fake Test"
        self.assertTrue(analyzer.match(self.obj))

    def test_multiple_words(self):
        analyzer = WordAnalyzer(None, None)
        self.assertEqual(analyzer.words, [])

        analyzer = WordAnalyzer(None, ["My", "first", "Test"])
        self.obj.body = "This is a little test for something"
        self.assertTrue(analyzer.match(self.obj))

        self.obj.body = "You are my best friend so far!"
        self.assertTrue(analyzer.match(self.obj))

        self.obj.body = "This is the first time I try this"
        self.assertTrue(analyzer.match(self.obj))

        self.obj.body = "This time we try to match multiple words/tests for the first time."
        self.assertTrue(analyzer.match(self.obj))

        self.obj.body = "None of the words are contained!"
        self.assertFalse(analyzer.match(self.obj))

        # Check for case sensitivity for multiple words
        analyzer2 = WordAnalyzer(None, ["My", "first", "Test"], case_sensitive=True)

        self.obj.body = "That's not my issue!"
        self.assertFalse(analyzer2.match(self.obj))

        self.obj.body = "That's not My issue!"
        self.assertTrue(analyzer2.match(self.obj))

    def test_add_word(self):
        analyzer = WordAnalyzer(None, "Test")
        self.assertEqual(len(analyzer.words), 1)
        self.assertEqual(analyzer.words, ["Test"])

        analyzer.add_word("second")
        self.assertEqual(len(analyzer.words), 2)
        self.assertEqual(analyzer.words, ["Test", "second"])

    def test_case_sensitive(self):
        analyzer = WordAnalyzer(None, "Test", case_sensitive=True)
        self.obj.body = "This is a Test for case sensitivity"
        self.assertTrue(analyzer.match(self.obj))

        self.obj.body = "This is a test for case sensitivity"
        self.assertFalse(analyzer.match(self.obj))

        self.obj.body = "This is a tESt for case sensitivity"
        self.assertFalse(analyzer.match(self.obj))

        analyzer2 = WordAnalyzer(None, "Te1st")
        self.obj.body = "This is a te1st for case sensitivity"
        self.assertTrue(analyzer2.match(self.obj))

        analyzer2 = WordAnalyzer(None, "Te1st")
        self.obj.body = "This is a tE1st for case sensitivity"
        self.assertTrue(analyzer2.match(self.obj))

    def test_multiple_case_sensitive(self):
        """Test if it's possible to match any of multiple words in a wordanalyzer when case sensitivty is activated"""
        analyzer = WordAnalyzer(None, ["My", "first", "Test"], case_sensitive=True)
        self.obj.body = "This is a little test for something"
        self.assertFalse(analyzer.match(self.obj))

        self.obj.body = "You are my best friend so far!"
        self.assertFalse(analyzer.match(self.obj))

        self.obj.body = "This is a Test for case sensitivity"
        self.assertTrue(analyzer.match(self.obj))

        self.obj.body = "This is a test for case sensitivity. It's the first of its kind."
        self.assertTrue(analyzer.match(self.obj))

    def test_match_none(self):
        analyzer = WordAnalyzer(None, "Test")
        self.obj.body = None
        self.assertFalse(analyzer.match(self.obj))

        self.obj = None
        self.assertFalse(analyzer.match(self.obj))

    def test_match_empty(self):
        analyzer = WordAnalyzer(None, "Test")
        self.obj.body = ""
        self.assertFalse(analyzer.match(self.obj))

    def test_actions_present(self):
        analyzer = WordAnalyzer(self.obj, "Test")
        self.assertEqual([self.obj], analyzer.actions)


if __name__ == '__main__':
    unittest.main()
