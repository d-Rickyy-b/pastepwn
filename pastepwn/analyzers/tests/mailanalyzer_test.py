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

    def test_match_negative(self):
        """Test if negatives are not recognized"""
        self.paste.body = ""
        self.assertFalse(self.analyzer.match(self.paste))
        self.paste.body = None
        self.assertFalse(self.analyzer.match(self.paste))
        self.paste.body = "This is a test without a mail@address anywhere"
        self.assertFalse(self.analyzer.match(self.paste))


if __name__ == '__main__':
    unittest.main()
