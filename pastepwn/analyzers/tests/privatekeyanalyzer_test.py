# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from pastepwn.analyzers.privatekeyanalyzer import PrivateKeyAnalyzer


class TestPrivateKeyAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = PrivateKeyAnalyzer(None)
        self.paste = mock.Mock()

    def test_match_positive(self):
        """Test if positives are recognized"""
        self.paste.body = "-----BEGIN PRIVATE KEY-----"
        self.assertTrue(self.analyzer.match(self.paste))
        self.paste.body = "-----BEGIN PGP PRIVATE KEY BLOCK-----"
        self.assertTrue(self.analyzer.match(self.paste))
        self.paste.body = "-----BEGIN RSA PRIVATE KEY-----"
        self.assertTrue(self.analyzer.match(self.paste))
        self.paste.body = "-----BEGIN ENCRYPTED PRIVATE KEY-----"
        self.assertTrue(self.analyzer.match(self.paste))
        self.paste.body = "-----BEGIN OPENSSH PRIVATE KEY-----"
        self.assertTrue(self.analyzer.match(self.paste))
        

    def test_match_negative(self):
        """Test if negatives are not recognized"""
        self.paste.body = ""
        self.assertFalse(self.analyzer.match(self.paste))
        self.paste.body = None
        self.assertFalse(self.analyzer.match(self.paste))
        self.paste.body = "-----BEGIN PUBLIC KEY-----"
        self.assertFalse(self.analyzer.match(self.paste))


if __name__ == '__main__':
    unittest.main()
