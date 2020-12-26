# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from pastepwn.analyzers.mailanalyzer import MailAnalyzer


class TestMailAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = MailAnalyzer(None)
        self.paste = mock.Mock()

    def test_match_positive(self):
        """Test if positives are recognized"""
        self.paste.body = "test@example.com"
        self.assertTrue(self.analyzer.match(self.paste))
        self.paste.body = "This is a test with a mail address in the end test@example.com"
        self.assertTrue(self.analyzer.match(self.paste))
        self.paste.body = "asdf@testmail.com This is a test with a mail address in the beginning"
        self.assertTrue(self.analyzer.match(self.paste))
        self.paste.body = "This is a test with a mail@address.com in the middle"
        self.assertTrue(self.analyzer.match(self.paste))

    def test_multiple(self):
        """Test if multiple matches are recognized"""
        self.paste.body = "This is a test with a mail@address.com in the middle. Also we\n" \
                          "want to have this asdf@testmail.com mail in here!"
        match = self.analyzer.match(self.paste)
        self.assertTrue(match)
        self.assertEqual(2, len(match))
        self.assertEqual("mail@address.com", match[0])
        self.assertEqual("asdf@testmail.com", match[1])

    def test_match_negative(self):
        """Test if negatives are not recognized"""
        self.paste.body = ""
        self.assertFalse(self.analyzer.match(self.paste))
        self.paste.body = None
        self.assertFalse(self.analyzer.match(self.paste))
        self.paste.body = "This is a test without a mail@address anywhere"
        self.assertFalse(self.analyzer.match(self.paste))


if __name__ == "__main__":
    unittest.main()
