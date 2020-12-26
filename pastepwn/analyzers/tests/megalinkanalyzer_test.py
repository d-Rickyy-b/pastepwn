# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from pastepwn.analyzers.megalinkanalyzer import MegaLinkAnalyzer


class TestMegaLinkAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = MegaLinkAnalyzer(None)
        self.paste = mock.Mock()

    def test_match_positive(self):
        """Test if positives are recognized"""
        # working mega link (short version)
        self.paste.body = "https://mega.nz/#F!XTQVEAZZ"
        self.assertTrue(self.analyzer.match(self.paste))

        # working mega link (medium version)
        self.paste.body = "https://mega.nz/#F!XTQVEAZZ!eqxlOvTxJKnvAkYvjC0O8g"
        self.assertTrue(self.analyzer.match(self.paste))

        # working mega link (long version)
        self.paste.body = "https://mega.nz/#F!PB8SSawR!SUokSlF2Zy8CR004DNFfNw!LQtniCoa"
        self.assertTrue(self.analyzer.match(self.paste))

        # without https header
        self.paste.body = "mega.nz/#F!XTQVEAZZ!eqxlOvTxJKnvAkYvjC0O8g"
        self.assertTrue(self.analyzer.match(self.paste))

        # http header
        self.paste.body = "http://mega.nz/#F!XTQVEAZZ!eqxlOvTxJKnvAkYvjC0O8g"
        self.assertTrue(self.analyzer.match(self.paste))

        # in a sentence
        self.paste.body = "check out this file:https://mega.nz/#F!PB8SSawR!SUokSlF2Zy8CR004DNFfNw!LQtniCoa"
        self.assertTrue(self.analyzer.match(self.paste))

        # multiple in one paste
        self.paste.body = "check out this file:https://mega.nz/#F!PB8SSawR!SUokSlF2Zy8CR004DNFfNw!LQtniCoa also use this link for other stuff:" \
                          "mega.nz/#F!XTQVEAZZ!eqxlOvTxJKnvAkYvjC0O8g"
        match = self.analyzer.match(self.paste)
        self.assertTrue(match)
        self.assertEqual("https://mega.nz/#F!PB8SSawR!SUokSlF2Zy8CR004DNFfNw!LQtniCoa", match[0])
        self.assertEqual("mega.nz/#F!XTQVEAZZ!eqxlOvTxJKnvAkYvjC0O8g", match[1])

    def test_match_negative(self):
        """Test if negatives are not recognized"""
        self.paste.body = ""
        self.assertFalse(self.analyzer.match(self.paste))

        self.paste.body = None
        self.assertFalse(self.analyzer.match(self.paste))

        # Invalid segment length
        self.paste.body = "https://mega.nz/#F!XTQVEAZZ1!eqxlOvTxJKnvAkYvjC0O8g"
        self.assertFalse(self.analyzer.match(self.paste))


if __name__ == "__main__":
    unittest.main()
