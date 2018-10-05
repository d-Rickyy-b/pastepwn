import unittest
from unittest import mock

from analyzers.ibananalyzer import IBANAnalyzer


class TestIBANAnalyzer(unittest.TestCase):
    def setUp(self):
        self.cut = IBANAnalyzer(None, True)

    def test_validation(self):
        self.assertTrue(self.cut._validate_iban("DE89 3704 0044 0532 0130 00"))
        self.assertTrue(self.cut._validate_iban("AT61 1904 3002 3457 3201"))
        self.assertTrue(self.cut._validate_iban("GB82-WEST-1234-5698-7654-32"))
        self.assertTrue(self.cut._validate_iban("NL20INGB0001234567"))

        self.assertFalse(self.cut._validate_iban("FR14 2004 1010 0505 0001 3"))
        self.assertFalse(self.cut._validate_iban("XX00 1234 5678 9012 3456 7890 1234 5678 90"))
        self.assertFalse(self.cut._validate_iban("YY00123456789012345678901234567890"))
        self.assertFalse(self.cut._validate_iban("XX22YYY1234567890123"))
        self.assertFalse(self.cut._validate_iban("foo@i.ban"))

    def test_match(self):
        obj = mock.Mock()
        obj.body = "This is inside DE89 3704 0044 0532 0130 00 a long paste"
        self.assertTrue(self.cut.match(obj))

        obj.body = "This is at the end DE89 3704 0044 0532 0130 00"
        self.assertTrue(self.cut.match(obj))


if __name__ == '__main__':
    unittest.main()
