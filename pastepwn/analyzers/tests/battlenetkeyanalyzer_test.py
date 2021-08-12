# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from pastepwn.analyzers.battlenetkeyanalyzer import BattleNetKeyAnalyzer


class TestBattleNetKeyAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = BattleNetKeyAnalyzer(None)
        self.paste = mock.Mock()

    def test_match_positive(self):
        """Test if positives are recognized"""
        # working battlenet key in 4-4-5-4-4 format
        self.paste.body = "NGM5-XB9P-8TLTR-V8BH-QFSW"
        self.assertTrue(self.analyzer.match(self.paste))
        self.assertEqual("NGM5-XB9P-8TLTR-V8BH-QFSW", self.analyzer.match(self.paste)[0])

        # key in 4-4-4-4 format
        self.paste.body = "MB9C-LV3C-4RG8-FME8"
        self.assertTrue(self.analyzer.match(self.paste))
        self.assertEqual("MB9C-LV3C-4RG8-FME8", self.analyzer.match(self.paste)[0])

        # part of a sentence
        self.paste.body = "Hey, I have your key right here: MB9C-LV3C-4RG8-FME8!"
        self.assertTrue(self.analyzer.match(self.paste))
        self.assertEqual("MB9C-LV3C-4RG8-FME8", self.analyzer.match(self.paste)[0])

        # Newline seperated keys
        self.paste.body = "MB9C-LV3C-4RG8-FME8\nNGM5-XB9P-8TLTR-V8BH-QFSW"
        self.assertTrue(self.analyzer.match(self.paste))
        self.assertEqual("MB9C-LV3C-4RG8-FME8", self.analyzer.match(self.paste)[0])
        self.assertEqual("NGM5-XB9P-8TLTR-V8BH-QFSW", self.analyzer.match(self.paste)[1])

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
