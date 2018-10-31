# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from pastepwn.analyzers.ibananalyzer import IBANAnalyzer


class TestIBANAnalyzer(unittest.TestCase):
    def setUp(self):
        self.cut = IBANAnalyzer(None, True)
        self.obj = mock.Mock()

    def test_validation_positive(self):
        self.assertTrue(self.cut._validate_iban("DE89 3704 0044 0532 0130 00"))
        self.assertTrue(self.cut._validate_iban("AT61 1904 3002 3457 3201"))
        self.assertTrue(self.cut._validate_iban("GB82-WEST-1234-5698-7654-32"))
        self.assertTrue(self.cut._validate_iban("NL20INGB0001234567"))

    def test_validation_negative(self):
        self.assertFalse(self.cut._validate_iban("FR14 2004 1010 0505 0001 3"))
        self.assertFalse(self.cut._validate_iban("XX00 1234 5678 9012 3456 7890 1234 5678 90"))
        self.assertFalse(self.cut._validate_iban("YY00123456789012345678901234567890"))
        self.assertFalse(self.cut._validate_iban("XX22YYY1234567890123"))
        self.assertFalse(self.cut._validate_iban("foo@i.ban"))

    def test_match_middle(self):
        self.obj.body = "This is inside DE89 3704 0044 0532 0130 00 a long paste."
        self.assertTrue(self.cut.match(self.obj))

    def test_match_end(self):
        self.obj.body = "This is at the beginning AT61 1904 3002 3457 3201"
        self.assertTrue(self.cut.match(self.obj))

    def test_match_beginning(self):
        self.obj.body = "NL20INGB0001234567 and this at the end."
        self.assertTrue(self.cut.match(self.obj))

    def test_match_single(self):
        self.obj.body = "GB82-WEST-1234-5698-7654-32"
        self.assertTrue(self.cut.match(self.obj))

    def test_match_multiple(self):
        self.obj.body = "This has DE89 3704 0044 0532 0130 00 two IBAN NL20INGB0001234567 in it."
        self.assertTrue(self.cut.match(self.obj))

    def test_match_validation(self):
        self.cut = IBANAnalyzer(None, False)
        self.obj.body = "This is inside FR14 2004 1010 0505 0001 3 a paste."
        self.assertTrue(self.cut.match(self.obj))

        self.cut = IBANAnalyzer(None, True)
        self.obj.body = "This is inside FR14 2004 1010 0505 0001 3 a paste."
        self.assertFalse(self.cut.match(self.obj))


if __name__ == '__main__':
    unittest.main()
