# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from pastepwn.analyzers.emailpasswordpairanalyzer import EmailPasswordPairAnalyzer


class TestEmailPasswordPairAnalyzer(unittest.TestCase):
    def setUp(self):
        self.obj = mock.Mock()

    def test_match(self):
        """Test single matches in a paste"""
        analyzer = EmailPasswordPairAnalyzer(None)
        self.obj.body = "This is a Test"
        self.assertFalse(analyzer.match(self.obj))

        analyzer = EmailPasswordPairAnalyzer(None)
        self.obj.body = "{a: 'b'}"
        self.assertFalse(analyzer.match(self.obj))

        analyzer = EmailPasswordPairAnalyzer(None)
        self.obj.body = ""
        self.assertFalse(analyzer.match(self.obj))

        analyzer = EmailPasswordPairAnalyzer(None)
        self.obj.body = "\t\n"
        self.assertFalse(analyzer.match(self.obj))

        analyzer = EmailPasswordPairAnalyzer(None)
        self.obj.body = "\n\n"
        self.assertFalse(analyzer.match(self.obj))

        analyzer = EmailPasswordPairAnalyzer(None)
        self.obj.body = "estocanam2@gmail.com:Firebird1@"
        self.assertTrue(analyzer.match(self.obj))

        analyzer = EmailPasswordPairAnalyzer(None)
        self.obj.body = "test+test@gmail.com:abcd"
        self.assertTrue(analyzer.match(self.obj))

        analyzer = EmailPasswordPairAnalyzer(None)
        self.obj.body = "estocanam2@gmail.com:aq12ws"
        self.assertTrue(analyzer.match(self.obj))

        analyzer = EmailPasswordPairAnalyzer(None)
        self.obj.body = "estocanam2@apple.com:Fireb§"
        self.assertTrue(analyzer.match(self.obj))

        analyzer = EmailPasswordPairAnalyzer(None)
        self.obj.body = "g@bb.com:Firebird1@"
        self.assertTrue(analyzer.match(self.obj))

    def test_match_multiple(self):
        """Test multiple matches in a single paste"""
        analyzer = EmailPasswordPairAnalyzer(None)
        self.obj.body = "estocanam2@apple.com:Fireb§\n" \
                        "g@bb.com:Firebird1@\n" \
                        "Some comment\n" \
                        "test+test@gmail.com:abcd"
        match = analyzer.match(self.obj)
        print(match)
        self.assertTrue(match)
        self.assertEqual("estocanam2@apple.com:Fireb§", match[0])
        self.assertEqual("g@bb.com:Firebird1@", match[1])
        self.assertEqual("test+test@gmail.com:abcd", match[2])

    def test_min_match(self):
        """Test if the setting for minimal matches works"""
        analyzer = EmailPasswordPairAnalyzer(None, min_amount=1)
        self.obj.body = "estocanam2@apple.com:Fireb§\n" \
                        "g@bb.com:Firebird1@\n" \
                        "Some comment\n" \
                        "test+test@gmail.com:abcd"
        self.assertEqual(3, len(analyzer.match(self.obj)))
        self.assertTrue(analyzer.match(self.obj))

        analyzer = EmailPasswordPairAnalyzer(None, min_amount=3)
        self.assertTrue(analyzer.match(self.obj))
        self.assertEqual(3, len(analyzer.match(self.obj)))

        analyzer = EmailPasswordPairAnalyzer(None, min_amount=4)
        self.assertFalse(analyzer.match(self.obj))
        self.assertEqual(bool, type(analyzer.match(self.obj)))


if __name__ == '__main__':
    unittest.main()
