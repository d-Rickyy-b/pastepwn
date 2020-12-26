# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from pastepwn.analyzers.epickeyanalyzer import EpicKeyAnalyzer


class TestEpicKeyAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = EpicKeyAnalyzer(None)
        self.paste = mock.Mock()

    def test_match_positive(self):
        """Test if positives are recognized"""
        # Epic key dump
        self.paste.body = "1GZJQ-DW7QX-SB4DC-THDW2"
        self.assertTrue(self.analyzer.match(self.paste))

        # Epic key dump
        self.paste.body = "KWETC-MK13P-4DO0N-VHT62"
        self.assertTrue(self.analyzer.match(self.paste))

        # Epic key dump
        self.paste.body = "MB9KG-TGXBJ-X8OXE-J7PIF"
        self.assertTrue(self.analyzer.match(self.paste))

        # Epic key dump
        self.paste.body = "OMYCF-Q9VYL-4FQEG-8F3XV"
        self.assertTrue(self.analyzer.match(self.paste))

        # part of a sentence
        self.paste.body = "Look it's FORTNITE! UGCTH-FH42S-OH98G-QHFZA"
        self.assertTrue(self.analyzer.match(self.paste))

        # Newline seperated Epic keys
        self.paste.body = "87C6Y-XIV2I-C3RJZ-B1SVZ\nQ8AQT-APT3F-MO7QU-KPE96"
        self.assertTrue(self.analyzer.match(self.paste))

    def test_match_negative(self):
        """Test if negatives are not recognized"""
        self.paste.body = ""
        self.assertFalse(self.analyzer.match(self.paste))

        self.paste.body = None
        self.assertFalse(self.analyzer.match(self.paste))

        # Invalid length in section
        self.paste.body = "Q8A5QT-APFT3F-MO74QU-KPEL96"
        self.assertFalse(self.analyzer.match(self.paste))

        # Too many segments
        self.paste.body = "1GZJQ-DW7QX-SB4DC-THDW2-1A2B3"
        self.assertFalse(self.analyzer.match(self.paste))

        # No separator
        self.paste.body = "OAPMCSEU6N7FFZ72AM5E"
        self.assertFalse(self.analyzer.match(self.paste))


if __name__ == "__main__":
    unittest.main()
