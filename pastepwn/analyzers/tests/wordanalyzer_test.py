# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from pastepwn.actions.basicaction import BasicAction
from pastepwn.analyzers.wordanalyzer import WordAnalyzer


class TestWordAnalyzer(unittest.TestCase):
    def setUp(self):
        self.paste = mock.Mock()

    def test_match(self):
        analyzer = WordAnalyzer(None, "Test")
        self.paste.body = "This is a Test"
        self.assertTrue(analyzer.match(self.paste))

        analyzer = WordAnalyzer(None, "Test")
        self.paste.body = "There are tests for everything"
        self.assertTrue(analyzer.match(self.paste))

        self.paste.body = "This is a Test for a longer sentence"
        self.assertTrue(analyzer.match(self.paste))

        self.paste.body = "Completely unrelated"
        self.assertFalse(analyzer.match(self.paste))

    def test_blacklist(self):
        blacklist = ["fake", "bad"]
        analyzer = WordAnalyzer(None, "Test", blacklist=blacklist)

        self.paste.body = "This is a Test"
        self.assertTrue(analyzer.match(self.paste))

        self.paste.body = "This is a fake Test"
        self.assertFalse(analyzer.match(self.paste))

        analyzer = WordAnalyzer(None, "Test", blacklist=blacklist, case_sensitive=True)

        self.paste.body = "This is a Test"
        self.assertTrue(analyzer.match(self.paste))

        self.paste.body = "This is a Fake Test"
        self.assertTrue(analyzer.match(self.paste))

    def test_multiple_words(self):
        analyzer = WordAnalyzer(None, None)
        self.assertEqual(analyzer.words, [])

        analyzer = WordAnalyzer(None, ["My", "first", "Test"])
        self.paste.body = "This is a little test for something"
        self.assertTrue(analyzer.match(self.paste))

        self.paste.body = "You are my best friend so far!"
        self.assertTrue(analyzer.match(self.paste))

        self.paste.body = "This is the first time I try this"
        self.assertTrue(analyzer.match(self.paste))

        self.paste.body = "This time we try to match multiple words/tests for the first time."
        self.assertTrue(analyzer.match(self.paste))

        self.paste.body = "None of the words are contained!"
        self.assertFalse(analyzer.match(self.paste))

        # Check for case sensitivity for multiple words
        analyzer2 = WordAnalyzer(None, ["My", "first", "Test"], case_sensitive=True)

        self.paste.body = "That's not my issue!"
        self.assertFalse(analyzer2.match(self.paste))

        self.paste.body = "That's not My issue!"
        self.assertTrue(analyzer2.match(self.paste))

    def test_add_word(self):
        analyzer = WordAnalyzer(None, "Test")
        self.assertEqual(len(analyzer.words), 1)
        self.assertEqual(["Test"], analyzer.words)

        analyzer.add_word("second")
        self.assertEqual(len(analyzer.words), 2)
        self.assertEqual(["Test", "second"], analyzer.words)

    def test_case_sensitive(self):
        analyzer = WordAnalyzer(None, "Test", case_sensitive=True)
        self.paste.body = "This is a Test for case sensitivity"
        self.assertTrue(analyzer.match(self.paste))

        self.paste.body = "This is a test for case sensitivity"
        self.assertFalse(analyzer.match(self.paste))

        self.paste.body = "This is a tESt for case sensitivity"
        self.assertFalse(analyzer.match(self.paste))

        analyzer2 = WordAnalyzer(None, "Te1st")
        self.paste.body = "This is a te1st for case sensitivity"
        self.assertTrue(analyzer2.match(self.paste))

        analyzer2 = WordAnalyzer(None, "Te1st")
        self.paste.body = "This is a tE1st for case sensitivity"
        self.assertTrue(analyzer2.match(self.paste))

    def test_multiple_case_sensitive(self):
        """Test if it's possible to match any of multiple words in a wordanalyzer when case sensitivty is activated"""
        analyzer = WordAnalyzer(None, ["My", "first", "Test"], case_sensitive=True)
        self.paste.body = "This is a little test for something"
        self.assertFalse(analyzer.match(self.paste))

        self.paste.body = "You are my best friend so far!"
        self.assertFalse(analyzer.match(self.paste))

        self.paste.body = "This is a Test for case sensitivity"
        match = analyzer.match(self.paste)
        self.assertTrue(match)
        self.assertEqual(1, len(match))
        self.assertEqual("Test", match[0])

        self.paste.body = "This is a test for case sensitivity. It's the first of its kind."
        match = analyzer.match(self.paste)
        self.assertTrue(match)
        self.assertEqual(1, len(match))
        self.assertEqual("first", match[0])

    def test_match_none(self):
        analyzer = WordAnalyzer(None, "Test")
        self.paste.body = None
        self.assertFalse(analyzer.match(self.paste))

        self.paste = None
        self.assertFalse(analyzer.match(self.paste))

    def test_match_empty(self):
        analyzer = WordAnalyzer(None, "Test")
        self.paste.body = ""
        self.assertFalse(analyzer.match(self.paste))

    def test_actions_present(self):
        action = mock.MagicMock(spec=BasicAction)
        analyzer = WordAnalyzer(action, "Test")
        self.assertEqual([action], analyzer.actions)


if __name__ == "__main__":
    unittest.main()
