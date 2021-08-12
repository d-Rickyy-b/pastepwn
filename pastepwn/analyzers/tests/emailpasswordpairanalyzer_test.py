# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from pastepwn.analyzers.emailpasswordpairanalyzer import EmailPasswordPairAnalyzer


class TestEmailPasswordPairAnalyzer(unittest.TestCase):
    def setUp(self):
        self.paste = mock.Mock()

    def test_positive(self):
        """Test single matches in a paste"""
        analyzer = EmailPasswordPairAnalyzer(None)
        self.paste.body = "estocanam2@gmail.com:Firebird1@"
        self.assertTrue(analyzer.match(self.paste))

        analyzer = EmailPasswordPairAnalyzer(None)
        self.paste.body = "test+test@gmail.com:abcd"
        self.assertTrue(analyzer.match(self.paste))

        analyzer = EmailPasswordPairAnalyzer(None)
        self.paste.body = "estocanam2@gmail.com:aq12ws"
        self.assertTrue(analyzer.match(self.paste))

        analyzer = EmailPasswordPairAnalyzer(None)
        self.paste.body = "estocanam2@apple.com:Fireb§"
        self.assertTrue(analyzer.match(self.paste))

        analyzer = EmailPasswordPairAnalyzer(None)
        self.paste.body = "g@bb.com:Firebird1@"
        self.assertTrue(analyzer.match(self.paste))

    def test_negative(self):
        """Tests if it does not match on wrong strings"""
        analyzer = EmailPasswordPairAnalyzer(None)
        self.paste.body = "This is a Test"
        self.assertFalse(analyzer.match(self.paste))

        analyzer = EmailPasswordPairAnalyzer(None)
        self.paste.body = "{a: 'b'}"
        self.assertFalse(analyzer.match(self.paste))

        analyzer = EmailPasswordPairAnalyzer(None)
        self.paste.body = ""
        self.assertFalse(analyzer.match(self.paste))

        analyzer = EmailPasswordPairAnalyzer(None)
        self.paste.body = "\t\n"
        self.assertFalse(analyzer.match(self.paste))

        analyzer = EmailPasswordPairAnalyzer(None)
        self.paste.body = "\n\n"
        self.assertFalse(analyzer.match(self.paste))

    def test_match_multiple(self):
        """Test multiple matches in a single paste"""
        analyzer = EmailPasswordPairAnalyzer(None)
        self.paste.body = "estocanam2@apple.com:Fireb§\n" \
                          "g@bb.com:Firebird1@\n" \
                          "Some comment\n" \
                          "test+test@gmail.com:abcd"
        match = analyzer.match(self.paste)
        self.assertTrue(match)
        self.assertEqual("estocanam2@apple.com:Fireb§", match[0])
        self.assertEqual("g@bb.com:Firebird1@", match[1])
        self.assertEqual("test+test@gmail.com:abcd", match[2])

    def test_min_match(self):
        """Test if the setting for minimal matches works"""
        analyzer = EmailPasswordPairAnalyzer(None, min_amount=1)
        self.paste.body = "estocanam2@apple.com:Fireb§\n" \
                          "g@bb.com:Firebird1@\n" \
                          "Some comment\n" \
                          "test+test@gmail.com:abcd"
        self.assertEqual(3, len(analyzer.match(self.paste)))
        self.assertTrue(analyzer.match(self.paste))

        analyzer = EmailPasswordPairAnalyzer(None, min_amount=3)
        self.assertTrue(analyzer.match(self.paste))
        self.assertEqual(3, len(analyzer.match(self.paste)))

        analyzer = EmailPasswordPairAnalyzer(None, min_amount=4)
        self.assertFalse(analyzer.match(self.paste))
        self.assertEqual(bool, type(analyzer.match(self.paste)))

    def test_intext(self):
        """Test if matches inside text are recognized"""
        analyzer = EmailPasswordPairAnalyzer(None)
        self.paste.body = "An email/pw combo estocanam2@apple.com:Fireb§ inside a text"
        match = analyzer.match(self.paste)
        self.assertTrue(match)
        self.assertEqual("estocanam2@apple.com:Fireb§", match[0])

        analyzer = EmailPasswordPairAnalyzer(None)
        self.paste.body = "also middle inside\nof test+test@gmail.com:abcd of a string!"
        match = analyzer.match(self.paste)
        self.assertTrue(match)
        self.assertEqual("test+test@gmail.com:abcd", match[0])

    def test_multiple(self):
        """Test if multiple matches are recognized"""
        analyzer = EmailPasswordPairAnalyzer(None)
        self.paste.body = "An email/pw combo estocanam2@apple.com:Fireb§ and also another inside\nof test+test@gmail.com:abcd of a string!"
        match = analyzer.match(self.paste)
        self.assertTrue(match)
        self.assertEqual("estocanam2@apple.com:Fireb§", match[0])
        self.assertEqual("test+test@gmail.com:abcd", match[1])


if __name__ == "__main__":
    unittest.main()
