# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from pastepwn.analyzers.googleoauthkeyanalyzer import GoogleOAuthKeyAnalyzer


class TestGoogleOAuthKeyAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = GoogleOAuthKeyAnalyzer(None)
        self.paste = mock.Mock()

    def test_match_positive(self):
        """Test if positives are recognized"""
        # google key dump
        self.paste.body = "6243-jhgcawesuycgaweiufyugfaiwyesfbaw.apps.googleusercontent.com"
        self.assertTrue(self.analyzer.match(self.paste))

        # google key dump
        self.paste.body = "6243-IUFHERIUFHASOEIRUFGHDOZIFUGVDHSF.apps.googleusercontent.com"
        self.assertTrue(self.analyzer.match(self.paste))

        # google key dump
        self.paste.body = "6243-18723612873612873621367128736128.apps.googleusercontent.com"
        self.assertTrue(self.analyzer.match(self.paste))

        # google key dump
        self.paste.body = "1-jhgcawesuycgaweiufyugfaiwyesfbaw.apps.googleusercontent.com"
        self.assertTrue(self.analyzer.match(self.paste))

        # google key dump
        self.paste.body = "6242345234234234234234234233-jhgcawesuycgaweiufyugfaiwyesfbaw.apps.googleusercontent.com"
        self.assertTrue(self.analyzer.match(self.paste))

    def test_match_negative(self):
        """Test if negatives are not recognized"""
        self.paste.body = ""
        self.assertFalse(self.analyzer.match(self.paste))

        self.paste.body = None
        self.assertFalse(self.analyzer.match(self.paste))

        # Invalid length
        self.paste.body = "6243-jhgcawesuycgaweiufyugfaisfbaw.apps.googleusercontent.com"
        self.assertFalse(self.analyzer.match(self.paste))

        # Invalid numbers
        self.paste.body = "-jhgcawesuycgaweiufyugfaiwyesfbaw.apps.googleusercontent.com"
        self.assertFalse(self.analyzer.match(self.paste))

        # Invalid domain
        self.paste.body = "6243-jhgcawesuycgaweiufyugfaiwyesfbaw.apps.google.com"
        self.assertFalse(self.analyzer.match(self.paste))


if __name__ == "__main__":
    unittest.main()
