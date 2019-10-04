# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from pastepwn.analyzers.emailpasswordpairanalyzer import EmailPasswordPairAnalyzer


class TestWordAnalyzer(unittest.TestCase):
    def setUp(self):
        self.obj = mock.Mock()

    def test_match(self):
        analyzer = EmailPasswordPairAnalyzer(None)
        self.obj.body = "This is a Test"
        self.assertFalse(analyzer.match(self.obj))

        analyzer = EmailPasswordPairAnalyzer(None)
        self.obj.body = "estocanam2@gmail.com:Firebird1@"
        self.assertTrue(analyzer.match(self.obj))


if __name__ == '__main__':
    unittest.main()
