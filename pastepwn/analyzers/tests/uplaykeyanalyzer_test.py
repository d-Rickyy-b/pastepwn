# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from pastepwn.analyzers.uplaykeyanalyzer import UplayKeyAnalyzer


class TestUplayKeyAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = UplayKeyAnalyzer(None)
        self.paste = mock.Mock()

    def test_match_positive(self):
        """Test if positives are recognized"""
        # working uplay key
        self.paste.body = "MB9C-LV3C-4RG8-FME8"
        self.assertTrue(self.analyzer.match(self.paste))

        # part of a sentence
        self.paste.body = "Hey, I have your key right here: MB9C-LV3C-4RG8-FME8!"
        self.assertTrue(self.analyzer.match(self.paste))

        # Newline seperated uplay key
        self.paste.body = "MB9C-LV3C-4RG8-FME8\nMB9C-LV3C-4RG8-FME8"
        match = self.analyzer.match(self.paste)
        self.assertTrue(match)
        self.assertEqual("MB9C-LV3C-4RG8-FME8", match[0])
        self.assertEqual("MB9C-LV3C-4RG8-FME8", match[1])

    def test_match_negative(self):
        """Test if negatives are not recognized"""
        self.paste.body = ""
        self.assertFalse(self.analyzer.match(self.paste))

        self.paste.body = None
        self.assertFalse(self.analyzer.match(self.paste))

        # Invalid length
        self.paste.body = "MB9AC-LV3C-4RG8-FME8"
        self.assertFalse(self.analyzer.match(self.paste))

        # Lower-case
        self.paste.body = "mb9c-lv3c-4rg8-fme8"
        self.assertFalse(self.analyzer.match(self.paste))


if __name__ == "__main__":
    unittest.main()
