# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from pastepwn.analyzers.ipv4addressanalyzer import IPv4AddressAnalyzer


class TestIPv4AddressAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = IPv4AddressAnalyzer([])
        self.paste = mock.Mock()

    def test_positive(self):
        self.paste.body = "255.255.255.255"
        self.assertTrue(self.analyzer.match(self.paste))
        self.paste.body = "255.255.255.0"
        self.assertTrue(self.analyzer.match(self.paste))
        self.paste.body = "10.0.0.1"
        self.assertTrue(self.analyzer.match(self.paste))
        self.paste.body = "127.0.0.1"
        self.assertTrue(self.analyzer.match(self.paste))

    def test_intext(self):
        """Test if matches inside text are recognized"""
        self.paste.body = "This is my private IP: 127.0.0.1 - this is secret!"
        match = self.analyzer.match(self.paste)
        self.assertTrue(match)
        self.assertEqual("127.0.0.1", match[0])

    def test_multiple(self):
        """Test if multiple matches are recognized"""
        self.paste.body = "This is my private IP: 127.0.0.1 - this is secret! Also my server's IP is 178.55.12.16"
        match = self.analyzer.match(self.paste)
        self.assertTrue(match)
        self.assertEqual("127.0.0.1", match[0])
        self.assertEqual("178.55.12.16", match[1])

    def test_negative(self):
        self.paste.body = "111.123.1232.123"
        self.assertFalse(self.analyzer.match(self.paste))
        self.paste.body = "1111.123.123.123"
        self.assertFalse(self.analyzer.match(self.paste))
        self.paste.body = "111.123.999.123"
        self.assertFalse(self.analyzer.match(self.paste))
        self.paste.body = "111.123.1232.123"
        self.assertFalse(self.analyzer.match(self.paste))


if __name__ == "__main__":
    unittest.main()
