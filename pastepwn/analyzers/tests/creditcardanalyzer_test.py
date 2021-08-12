# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from pastepwn.analyzers.creditcardanalyzer import CreditCardAnalyzer


class TestCreditCardAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = CreditCardAnalyzer(None)
        self.paste = mock.Mock()

    def test_match_positive(self):
        """Test if positives are recognized
        * CARDS IN ORDER *
        VISA
        MASTERCARD
        AMERICAN EXPRESS
        DINERS CLUB
        DISCOVER
        JCB
        """
        self.paste.body = "4556316812657526"
        self.assertTrue(self.analyzer.match(self.paste))
        self.paste.body = "4556 3168 1265 7526"
        self.assertTrue(self.analyzer.match(self.paste))

        self.paste.body = "5168441223630339"
        self.assertTrue(self.analyzer.match(self.paste))
        self.paste.body = "5168 4412 2363 0339"
        self.assertTrue(self.analyzer.match(self.paste))

        self.paste.body = "371642190784801"
        self.assertTrue(self.analyzer.match(self.paste))
        self.paste.body = "3716 421907 84801"
        self.assertTrue(self.analyzer.match(self.paste))

        self.paste.body = "30043277253249"
        self.assertTrue(self.analyzer.match(self.paste))
        self.paste.body = "3004 327725 3249"
        self.assertTrue(self.analyzer.match(self.paste))

        self.paste.body = "6011988461284820"
        self.assertTrue(self.analyzer.match(self.paste))
        self.paste.body = "6011 9884 6128 4820"
        self.assertTrue(self.analyzer.match(self.paste))

        self.paste.body = "3538684728624673"
        self.assertTrue(self.analyzer.match(self.paste))
        self.paste.body = "3538 6847 2862 4673"
        self.assertTrue(self.analyzer.match(self.paste))

    def test_match_negative(self):
        """Test if negatives are not recognized"""
        self.paste.body = ""
        self.assertFalse(self.analyzer.match(self.paste))
        self.paste.body = None
        self.assertFalse(self.analyzer.match(self.paste))
        self.paste.body = "https://www.github.com"
        self.assertFalse(self.analyzer.match(self.paste))
        self.paste.body = "1234 5678 9101 12"
        self.assertFalse(self.analyzer.match(self.paste))
        self.paste.body = "123456789101112"
        self.assertFalse(self.analyzer.match(self.paste))
        self.paste.body = "51684+4122363339"
        self.assertFalse(self.analyzer.match(self.paste))
        self.paste.body = "+5168441223630"
        self.assertFalse(self.analyzer.match(self.paste))
        self.paste.body = "5368441223630339183239284"
        self.assertFalse(self.analyzer.match(self.paste))


if __name__ == "__main__":
    unittest.main()
