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
        self.paste.body = "-----BEGIN PRIVATE KEY-----asdasdasdfgsdfgdfgs-----END PRIVATE KEY-----"
        self.assertTrue(self.analyzer.match(self.paste))
        self.paste.body = "-----BEGIN PGP PRIVATE KEY BLOCK-----ZzEF0RDWWYb1vPTIeNrKrMEOZ+LesRil6TXCn5/4I0VinlrnVpRbF4xtsVt4eIRkomN9eN-----END PGP PRIVATE " \
                          "KEY BLOCK-----"
        self.assertTrue(self.analyzer.match(self.paste))
        self.paste.body = "-----BEGIN RSA PRIVATE KEY-----sRefW7LzPMmTgqHgbNv/gTtT4V/Tc1CiYGVtG9NPlP9tAAAIAI/WvZ3Clh+B0X9mkZ9-----END RSA PRIVATE KEY-----"
        self.assertTrue(self.analyzer.match(self.paste))
        self.paste.body = "-----BEGIN ENCRYPTED PRIVATE KEY-----sRefW7LzPMmTgqHgbNv/gTtT4V/Tc1CiYGVtG9NPlP9tAAAIAI/WvZ3Clh+B0X9mkZ9-----END ENCRYPTED " \
                          "PRIVATE KEY-----"
        self.assertTrue(self.analyzer.match(self.paste))
        self.paste.body = "-----BEGIN OPENSSH PRIVATE KEY-----sRefW7LzPMmTgqHgbNv/gTtT4V/Tc1CiYGVtG9NPlP9tAAAIAI/WvZ3Clh+B0X9mkZ9-----END OPENSSH " \
                          "PRIVATE KEY-----"
        self.assertTrue(self.analyzer.match(self.paste))

    def test_match_negative(self):
        """Test if negatives are not recognized"""
        self.paste.body = ""
        self.assertFalse(self.analyzer.match(self.paste))
        self.paste.body = None
        self.assertFalse(self.analyzer.match(self.paste))
        self.paste.body = "-----BEGIN PUBLIC KEY-----"
        self.assertFalse(self.analyzer.match(self.paste))


if __name__ == "__main__":
    unittest.main()
