# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from pastepwn.analyzers.md5hashanalyzer import MD5HashAnalyzer


class TestMD5HashAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = MD5HashAnalyzer(None)
        self.paste = mock.Mock()

    def test_match_positive(self):
        """Test if positives are recognized"""
        # md5 hash of 128 character string: ndq=S)t<5dgQhD7rCyAZ<?k,b&Zh-t^@'d=kaf:tK$PH\8HSzt%q9pX&RsGuYAcnmy9Rh!'(9sWt.d&\hS,LSA4>#Gn@sYn``5Tt6X`h'Hn_Y-"F>DkGr'\/:4kLF:D"
        self.paste.body = "5812c57a01b5efa30af09d4f9388e50d"
        self.assertTrue(self.analyzer.match(self.paste))

        # md5 hash of 64 character string: sa.tpMvv#J{q)tZfz,W[5Hq*Yz%kN(,8j)p>'g["d^mSLHkD)gZLVxk/,}#aVxv*
        self.paste.body = "372f202bdf0f16dfa41c101fc6a41695"
        self.assertTrue(self.analyzer.match(self.paste))

        # md5 hash of 32 character string: zw8hspDAZ(\w]K/v~yZaa_m$6awgF4rj
        self.paste.body = "2287c6975240f865a9945ec9bcc0eead"
        self.assertTrue(self.analyzer.match(self.paste))

        # md5 hash of 16 character string: cY4>szK'>(?48tz=
        self.paste.body = "f2195cea00cc796676f77b9d19473f7a"
        self.assertTrue(self.analyzer.match(self.paste))

        self.paste.body = "my super cool hash is 2287c6975240f865a9945ec9bcc0eead and here's some more text"
        self.assertTrue(self.analyzer.match(self.paste))

        # Newline-separated valid hashes
        self.paste.body = "2287c6975240f865a9945ec9bcc0eead\n372f202bdf0f16dfa41c101fc6a41695"
        self.assertTrue(self.analyzer.match(self.paste))

    def test_match_negative(self):
        """Test if negatives are not recognized"""
        self.paste.body = ""
        self.assertFalse(self.analyzer.match(self.paste))

        self.paste.body = None
        self.assertFalse(self.analyzer.match(self.paste))

        # Invalid character 'g'
        self.paste.body = "f2195cea00cc796676f77b9d19473f7g"
        self.assertFalse(self.analyzer.match(self.paste))

        # SHA Hash
        self.paste.body = "f1d2d2f924e986ac86fdf7b36c94bcdf32beec15"
        self.assertFalse(self.analyzer.match(self.paste))

        # Invalid MD5 hash length
        self.paste.body = "f2195cea00cc796676f77b9d19473f7"
        self.assertFalse(self.analyzer.match(self.paste))


if __name__ == "__main__":
    unittest.main()
