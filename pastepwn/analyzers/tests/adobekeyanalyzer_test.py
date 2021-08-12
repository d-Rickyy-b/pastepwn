# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from pastepwn.analyzers.adobekeyanalyzer import AdobeKeyAnalyzer


class TestAdobeKeyAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = AdobeKeyAnalyzer(None)
        self.paste = mock.Mock()

    def test_match_positive(self):
        """Test if positives are recognized"""
        # adobe key dump
        self.paste.body = "1118-1993-2045-6322-6067-9110"
        self.assertTrue(self.analyzer.match(self.paste))
        self.assertEqual("1118-1993-2045-6322-6067-9110", self.analyzer.match(self.paste)[0])

        # adobe key dump
        self.paste.body = "1118-1551-7298-8490-8910-4435"
        self.assertTrue(self.analyzer.match(self.paste))
        self.assertEqual("1118-1551-7298-8490-8910-4435", self.analyzer.match(self.paste)[0])

        # adobe key dump
        self.paste.body = "1118-1088-9818-3636-2479-0297"
        self.assertTrue(self.analyzer.match(self.paste))
        self.assertEqual("1118-1088-9818-3636-2479-0297", self.analyzer.match(self.paste)[0])

        # adobe key dump
        self.paste.body = "1118-1194-1581-4556-8113-6593"
        self.assertTrue(self.analyzer.match(self.paste))
        self.assertEqual("1118-1194-1581-4556-8113-6593", self.analyzer.match(self.paste)[0])

        # part of a sentence
        self.paste.body = "Hey, I have your key right here: 1118-1470-8779-0264-4009-3244!"
        self.assertTrue(self.analyzer.match(self.paste))
        self.assertEqual("1118-1470-8779-0264-4009-3244", self.analyzer.match(self.paste)[0])

        # Newline seperated microsoft key
        self.paste.body = "1118-1993-2046-6322-6067-9110\n1118-1470-8779-0264-4009-3244"
        self.assertTrue(self.analyzer.match(self.paste))
        self.assertEqual("1118-1993-2046-6322-6067-9110", self.analyzer.match(self.paste)[0])
        self.assertEqual("1118-1470-8779-0264-4009-3244", self.analyzer.match(self.paste)[1])

    def test_match_negative(self):
        """Test if negatives are not recognized"""
        self.paste.body = ""
        self.assertFalse(self.analyzer.match(self.paste))

        self.paste.body = None
        self.assertFalse(self.analyzer.match(self.paste))

        # Invalid length
        self.paste.body = "1118-1470-8779-0264-4009-32445"
        self.assertFalse(self.analyzer.match(self.paste))
        self.assertEqual(list, type(self.analyzer.match(self.paste)))

        # Invalid length
        self.paste.body = "1118-1470-8779-0264-4009-324"
        self.assertFalse(self.analyzer.match(self.paste))
        self.assertEqual(list, type(self.analyzer.match(self.paste)))

        # Invalid Characters
        self.paste.body = "1118-1194-1581-4556-8113-659A"
        self.assertFalse(self.analyzer.match(self.paste))
        self.assertEqual(list, type(self.analyzer.match(self.paste)))


if __name__ == "__main__":
    unittest.main()
