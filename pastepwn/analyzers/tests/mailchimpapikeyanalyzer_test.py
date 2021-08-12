# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from pastepwn.analyzers.mailchimpapikeyanalyzer import MailChimpApiKeyAnalyzer


class TestMailChimpApiKeyAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = MailChimpApiKeyAnalyzer(None)
        self.paste = mock.Mock()

    def test_match_positive(self):
        """Test if positives are recognized"""
        self.paste.body = "87b6ac876aca87c687a6c87a6ca876c8-us000000000000"
        self.assertTrue(self.analyzer.match(self.paste))
        self.paste.body = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa-us000000000000"
        self.assertTrue(self.analyzer.match(self.paste))
        self.paste.body = "12312312312312312312312312312312-us000000000000"
        self.assertTrue(self.analyzer.match(self.paste))
        self.paste.body = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa-us345646456456"
        self.assertTrue(self.analyzer.match(self.paste))

    def test_match_negative(self):
        """Test if negatives are not recognized"""
        self.paste.body = ""
        self.assertFalse(self.analyzer.match(self.paste))
        self.paste.body = None
        self.assertFalse(self.analyzer.match(self.paste))
        self.paste.body = "asdasdasdasdasdasdasdasdasdasdas-us000000000000"
        self.assertFalse(self.analyzer.match(self.paste))
        self.paste.body = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa-it000000000000"
        self.assertFalse(self.analyzer.match(self.paste))
        self.paste.body = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa-usasdasdasdasd"
        self.assertFalse(self.analyzer.match(self.paste))


if __name__ == "__main__":
    unittest.main()
