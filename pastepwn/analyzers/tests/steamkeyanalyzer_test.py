# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from pastepwn.analyzers.steamkeyanalyzer import SteamKeyAnalyzer


class TestSteamKeyAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = SteamKeyAnalyzer(None)
        self.paste = mock.Mock()

    def test_match_positive(self):
        """Test if positives are recognized"""
        # steam key dump
        self.paste.body = "EZFNY-7GECB-94WRD"
        self.assertTrue(self.analyzer.match(self.paste))

        # steam key dump
        self.paste.body = "10NL7-7E8VK-ZUSOD"
        self.assertTrue(self.analyzer.match(self.paste))

        # steam key dump
        self.paste.body = "CB6AW-XHHB1-IANNO"
        self.assertTrue(self.analyzer.match(self.paste))

        # steam key dump
        self.paste.body = "E4XJ8-2MRI0-RX4I5"
        self.assertTrue(self.analyzer.match(self.paste))

        # part of a sentence
        self.paste.body = "Hey, I have your key right here: EL0SY-DC710-X0C5W!"
        self.assertTrue(self.analyzer.match(self.paste))

        # Newline seperated steam key
        self.paste.body = "E4XJ8-2MRI0-RX4I5\nCIZ36-WD38P-QZI6U"
        self.assertTrue(self.analyzer.match(self.paste))

    def test_match_negative(self):
        """Test if negatives are not recognized"""
        self.paste.body = ""
        self.assertFalse(self.analyzer.match(self.paste))

        self.paste.body = None
        self.assertFalse(self.analyzer.match(self.paste))

        # Invalid length
        self.paste.body = "CBCB6AW-XHHB1-IANNO"
        self.assertFalse(self.analyzer.match(self.paste))

        # Lower-case
        self.paste.body = "e4xj8-2mri0-rx4i5"
        self.assertFalse(self.analyzer.match(self.paste))


if __name__ == '__main__':
    unittest.main()
