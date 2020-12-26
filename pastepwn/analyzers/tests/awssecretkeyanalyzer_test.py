# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from pastepwn.analyzers.awssecretkeyanalyzer import AWSSecretKeyAnalyzer


class TestAWSSecretKeyAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = AWSSecretKeyAnalyzer(None)
        self.paste = mock.Mock()

    def test_match_positive(self):
        """Test if positives are recognized"""
        # obtained by pastebin search
        self.paste.body = "HrNMIhjZDnvkH5YGJpwjq0Flmj8H+dvURedLRjsO"
        self.assertTrue(self.analyzer.match(self.paste))

        # obtained by pastebin search
        self.paste.body = "ZGBMmoyRxdhMObx0EuANS9FiS2kG5FwDVLH2XY7y"
        self.assertTrue(self.analyzer.match(self.paste))

        # obtained by pastebin search
        self.paste.body = "kYKQ24NoNtmga55G7OVeY/kPAZ7xONl6FfmuXArc"
        self.assertTrue(self.analyzer.match(self.paste))

        # obtained by pastebin search
        self.paste.body = "9cf95dacd226dcf43da376cdb6cbba7035218921"
        self.assertTrue(self.analyzer.match(self.paste))

    def test_match_intext(self):
        """Test if matches inside text are recognized"""
        self.paste.body = "my super cool hash is 9cf95dacd226dcf43da376cdb6cbba7035218921 and here's some more text"
        match = self.analyzer.match(self.paste)
        self.assertTrue(match)
        self.assertEqual("9cf95dacd226dcf43da376cdb6cbba7035218921", match[0])

        self.paste.body = "AWS Secret Access Key [None]: HrNMIhjZDnvkH5YGJpwjq0Flmj8H+dvURedLRjsO"
        match = self.analyzer.match(self.paste)
        self.assertTrue(match)
        self.assertEqual("HrNMIhjZDnvkH5YGJpwjq0Flmj8H+dvURedLRjsO", match[0])

    def test_multiple(self):
        """Test if multiple matches are recognized"""
        # Newline-separated valid hashes
        self.paste.body = "ZGBMmoyRxdhMObx0EuANS9FiS2kG5FwDVLH2XY7y\nHrNMIhjZDnvkH5YGJpwjq0Flmj8H+dvURedLRjsO"
        match = self.analyzer.match(self.paste)
        self.assertTrue(match)
        self.assertEqual("ZGBMmoyRxdhMObx0EuANS9FiS2kG5FwDVLH2XY7y", match[0])
        self.assertEqual("HrNMIhjZDnvkH5YGJpwjq0Flmj8H+dvURedLRjsO", match[1])

    def test_match_negative(self):
        """Test if negatives are not recognized"""
        self.paste.body = ""
        self.assertFalse(self.analyzer.match(self.paste))

        self.paste.body = None
        self.assertFalse(self.analyzer.match(self.paste))

        # Invalid character '-'
        self.paste.body = "9cf95dacd226dcf43da376cdb6cbb-7035218921"
        self.assertFalse(self.analyzer.match(self.paste))

        # MD5 Hash
        self.paste.body = "9e107d9d372bb6826bd81d3542a419d6"
        self.assertFalse(self.analyzer.match(self.paste))

        # Invalid length
        self.paste.body = "ZGBMmoyRxdhMObx0EuANS9FiS2kG5FwDVLH2XY7y1"
        self.assertFalse(self.analyzer.match(self.paste))
        self.paste.body = "ZGBMmoyRxdhMObx0EuANS9FiS2kG5FwDVLH2XY7"
        self.assertFalse(self.analyzer.match(self.paste))


if __name__ == "__main__":
    unittest.main()
