# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from pastepwn.analyzers.phonenumberanalyzer import PhoneNumberAnalyzer


class TestPhoneNumberAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = PhoneNumberAnalyzer(None)
        self.paste = mock.Mock()

    def test_match_positive(self):
        """Test if positives are recognized"""
        self.paste.body = "+14155552671"
        self.assertTrue(self.analyzer.match(self.paste))
        self.paste.body = "+1 4155552671"
        self.assertTrue(self.analyzer.match(self.paste))
        self.paste.body = "+49 89-636-48018"
        self.assertTrue(self.analyzer.match(self.paste))
        self.paste.body = "+357  81-127 29103"
        self.assertTrue(self.analyzer.match(self.paste))
        self.paste.body = "+1 (811) 1272 103"
        self.assertTrue(self.analyzer.match(self.paste))

    def test_intext(self):
        """Test if matches inside text are recognized"""
        self.paste.body = "Check out my new number: +1 (811) 1272 103 this is it"
        match = self.analyzer.match(self.paste)
        self.assertTrue(match)
        self.assertEqual("+1 (811) 1272 103", match[0])

    def test_multiple(self):
        """Test if multiple matches are recognized"""
        self.paste.body = "Check out all those numbers: +1 (811) 1272 103\n+357  81-127 29103 and many more"
        match = self.analyzer.match(self.paste)
        self.assertTrue(match)
        self.assertEqual("+1 (811) 1272 103", match[0])
        self.assertEqual("+357  81-127 29103", match[1])

    def test_match_negative(self):
        """Test if negatives are not recognized"""
        self.paste.body = ""
        self.assertFalse(self.analyzer.match(self.paste))
        self.paste.body = None
        self.assertFalse(self.analyzer.match(self.paste))
        self.paste.body = "https://www.google.com"
        self.assertFalse(self.analyzer.match(self.paste))
        self.paste.body = "123456789"
        self.assertFalse(self.analyzer.match(self.paste))
        self.paste.body = "123 456 789"
        self.assertFalse(self.analyzer.match(self.paste))
        self.paste.body = "+42"
        self.assertFalse(self.analyzer.match(self.paste))
        self.paste.body = "+42 1"
        self.assertFalse(self.analyzer.match(self.paste))
        self.paste.body = "+123456789012345678901234567890"
        self.assertFalse(self.analyzer.match(self.paste))


if __name__ == "__main__":
    unittest.main()
