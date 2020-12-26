# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from pastepwn.analyzers.microsoftkeyanalyzer import MicrosoftKeyAnalyzer


class TestMicrosoftKeyAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = MicrosoftKeyAnalyzer(None)
        self.paste = mock.Mock()

    def test_match_positive(self):
        """Test if positives are recognized"""
        # microsoft key dump
        self.paste.body = "2YM6W-NXCWB-RX6F2-QFVDW-J8C9V"
        self.assertTrue(self.analyzer.match(self.paste))

        # microsoft key dump
        self.paste.body = "6N667-BMRDR-T2WMM-2RMQ9-DYF3H"
        self.assertTrue(self.analyzer.match(self.paste))

        # microsoft key dump
        self.paste.body = "88PNQ-KF99B-VJG64-R28RW-D9JQH"
        self.assertTrue(self.analyzer.match(self.paste))

        # microsoft key dump
        self.paste.body = "BNQWW-X4422-FCXD8-JPT37-PWC9V"
        self.assertTrue(self.analyzer.match(self.paste))

        # part of a sentence
        self.paste.body = "Hey, I have your key right here: GC288-NVPMT-GWF2M-76228-W42DH!"
        self.assertTrue(self.analyzer.match(self.paste))

        # Newline seperated microsoft key
        self.paste.body = "N3B2Q-F9GQF-PTDBG-KKRR7-7QTXV\nN6C37-P8DW3-YVG9X-BRW77-9BQ67"
        match = self.analyzer.match(self.paste)
        self.assertTrue(match)
        self.assertTrue("N3B2Q-F9GQF-PTDBG-KKRR7-7QTXV", match[0])
        self.assertTrue("N6C37-P8DW3-YVG9X-BRW77-9BQ67", match[1])

    def test_match_negative(self):
        """Test if negatives are not recognized"""
        self.paste.body = ""
        self.assertFalse(self.analyzer.match(self.paste))

        self.paste.body = None
        self.assertFalse(self.analyzer.match(self.paste))

        # Invalid length
        self.paste.body = "PNT6B-DKH2Q-GW4J2-DDT6T-PDHT76"
        self.assertFalse(self.analyzer.match(self.paste))

        # Invalid length
        self.paste.body = "PNT6B-DKH2Q-GW4J2-DDT6T-PDHT"
        self.assertFalse(self.analyzer.match(self.paste))

        # Invalid Characters
        self.paste.body = "A78QN-Y8XXR-MKFK7-Q4R6C-Q3TXV"
        self.assertFalse(self.analyzer.match(self.paste))


if __name__ == "__main__":
    unittest.main()
