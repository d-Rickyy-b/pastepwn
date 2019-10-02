# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from pastepwn.analyzers.dbconnstringanalyser import DBConnAnalyser


class TestDBConnAnalyser(unittest.TestCase):
    def setUp(self):
        self.analyzer = DBConnAnalyser(None)
        self.paste = mock.Mock()

    def test_match_positive(self):
        """Test if positives are recognized"""
        self.paste.body = "cassandra://194.3.5.2"
        self.assertTrue(self.analyzer.match(self.paste))
        self.paste.body = "postgresql://user:secret@localhost"
        self.assertTrue(self.analyzer.match(self.paste))
        self.paste.body = "mongodb://router1.example.com:27017"
        self.assertTrue(self.analyzer.match(self.paste))

    def test_match_negative(self):
        """Test if negatives are not recognized"""
        self.paste.body = ""
        self.assertFalse(self.analyzer.match(self.paste))
        self.paste.body = None
        self.assertFalse(self.analyzer.match(self.paste))
        self.paste.body = "https://www.google.com"
        self.assertFalse(self.analyzer.match(self.paste))


if __name__ == '__main__':
    unittest.main()
