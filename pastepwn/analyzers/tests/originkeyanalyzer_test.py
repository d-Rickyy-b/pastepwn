# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from pastepwn.analyzers.originkeyanalyzer import OriginKeyAnalyzer


class TestOriginKeyAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = OriginKeyAnalyzer(None)
        self.paste = mock.Mock()

    def test_match_positive(self):
        """Test if positives are recognized"""
        # origin key dump
        self.paste.body = "87NN-Z277-KTHD-EDJL-7MVB"
        self.assertTrue(self.analyzer.match(self.paste))

        # origin key dump
        self.paste.body = "DPMV-FZXD-GD2G-7U28-6S3D"
        self.assertTrue(self.analyzer.match(self.paste))

        # origin key dump
        self.paste.body = "ACT3-3TD6-ZDYB-BCGP-TTDM"
        self.assertTrue(self.analyzer.match(self.paste))

        # origin key dump
        self.paste.body = "63WW-8VQE-7VEA-HFCD-LVYT"
        self.assertTrue(self.analyzer.match(self.paste))

        # part of a sentence
        self.paste.body = "Hey, I have your key right here: 87NN-Z277-KTHD-EDJL-7MVB!"
        self.assertTrue(self.analyzer.match(self.paste))

        # Newline seperated origin key
        self.paste.body = "87NN-Z277-KTHD-EDJL-7MVB\nDPMV-FZXD-GD2G-7U28-6S3D"
        match = self.analyzer.match(self.paste)
        self.assertTrue(match)
        self.assertEqual("87NN-Z277-KTHD-EDJL-7MVB", match[0])
        self.assertEqual("DPMV-FZXD-GD2G-7U28-6S3D", match[1])

    def test_match_negative(self):
        """Test if negatives are not recognized"""
        self.paste.body = ""
        self.assertFalse(self.analyzer.match(self.paste))

        self.paste.body = None
        self.assertFalse(self.analyzer.match(self.paste))

        # Invalid length
        self.paste.body = "A63WW-8VQE-7VEA-HFCD-LVYT"
        self.assertFalse(self.analyzer.match(self.paste))

        # Invalid Characters
        self.paste.body = "63W_-8VQE-7VEA-HFCD-LVYT"
        self.assertFalse(self.analyzer.match(self.paste))


if __name__ == "__main__":
    unittest.main()
