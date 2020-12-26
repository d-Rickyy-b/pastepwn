# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from pastepwn.analyzers.dbconnstringanalyzer import DBConnAnalyzer


class TestDBConnAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = DBConnAnalyzer(None)
        self.paste = mock.Mock()

    def test_match_positive(self):
        """Test if positives are recognized"""
        self.paste.body = "cassandra://194.3.5.2"
        self.assertTrue(self.analyzer.match(self.paste))
        self.assertEqual("cassandra://194.3.5.2", self.analyzer.match(self.paste)[0])

        self.paste.body = "postgresql://user:secret@localhost"
        self.assertTrue(self.analyzer.match(self.paste))
        self.assertEqual("postgresql://user:secret@localhost", self.analyzer.match(self.paste)[0])

        self.paste.body = "mongodb://router1.example.com:27017"
        self.assertTrue(self.analyzer.match(self.paste))
        self.assertEqual("mongodb://router1.example.com:27017", self.analyzer.match(self.paste)[0])

        self.paste.body = "The db connection string is 'mongodb://router1.example.com:27017' but please keep this for yourself!"
        self.assertTrue(self.analyzer.match(self.paste))
        self.assertEqual("mongodb://router1.example.com:27017", self.analyzer.match(self.paste)[0])

    def test_match_multiple(self):
        self.paste.body = "The db connection string is 'mongodb://router1.example.com:27017' but please keep this for yourself! Also make sure to use " \
                          "postgresql://user:secret@localhost as postgres connection"
        match = self.analyzer.match(self.paste)
        self.assertTrue(match)
        self.assertEqual(2, len(match))
        self.assertEqual("mongodb://router1.example.com:27017", match[0])
        self.assertEqual("postgresql://user:secret@localhost", match[1])

    def test_match_negative(self):
        """Test if negatives are not recognized"""
        self.paste.body = ""
        self.assertFalse(self.analyzer.match(self.paste))
        self.paste.body = None
        self.assertFalse(self.analyzer.match(self.paste))
        self.paste.body = "https://www.google.com"
        self.assertFalse(self.analyzer.match(self.paste))
        self.paste.body = "http://www.google.com"
        self.assertFalse(self.analyzer.match(self.paste))


if __name__ == "__main__":
    unittest.main()
