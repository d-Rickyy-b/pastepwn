# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from pastepwn.analyzers.emailpasswordpairanalyzer import EmailPasswordPairAnalyzer


class TestEmailPasswordPairAnalyzer(unittest.TestCase):
    def setUp(self):
        self.obj = mock.Mock()

    def test_match(self):
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


if __name__ == '__main__':
    unittest.main()
