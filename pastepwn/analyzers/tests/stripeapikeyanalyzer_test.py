# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from pastepwn.analyzers.stripeapikeyanalyzer import StripeApiKeyAnalyzer


class TestStripeApiKeyAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = StripeApiKeyAnalyzer(None)
        self.paste = mock.Mock()

    def test_match_positive(self):
        """Test if positives are recognized"""
        # steam key dump
        self.paste.body = "sk_test_4fsrdffsdf345345dfgfg34i"
        self.assertTrue(self.analyzer.match(self.paste))

        # steam key dump
        self.paste.body = "rk_test_4fsrdffsdf345345dfgfg34i"
        self.assertTrue(self.analyzer.match(self.paste))

        # steam key dump
        self.paste.body = "sk_live_4fsrdffsdf345345dfgfg34i"
        self.assertTrue(self.analyzer.match(self.paste))

        # steam key dump
        self.paste.body = "rk_live_4fsrdffsdf345345dfgfg34i"
        self.assertTrue(self.analyzer.match(self.paste))

        # steam key dump
        self.paste.body = "sk_test_YUTGF76uyh876Tyg87T786Tu"
        self.assertTrue(self.analyzer.match(self.paste))

    def test_match_negative(self):
        """Test if negatives are not recognized"""
        self.paste.body = ""
        self.assertFalse(self.analyzer.match(self.paste))

        self.paste.body = None
        self.assertFalse(self.analyzer.match(self.paste))

        # Invalid length
        self.paste.body = "sk_test_YUTGF76uyh876"
        self.assertFalse(self.analyzer.match(self.paste))

        # Invalid first letter
        self.paste.body = "pk_test_YUTGF76uyh876Tyg87T786Tu"
        self.assertFalse(self.analyzer.match(self.paste))

        # Invalid state
        self.paste.body = "sk_staging_YUTGF76uyh876Tyg87T786Tu"
        self.assertFalse(self.analyzer.match(self.paste))


if __name__ == '__main__':
    unittest.main()
