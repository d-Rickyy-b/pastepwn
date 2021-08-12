# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from pastepwn.analyzers.awssessiontokenanalyzer import AWSSessionTokenAnalyzer


class TestAWSSessionTokenAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = AWSSessionTokenAnalyzer(None)
        self.paste = mock.Mock()

    def test_mach_positive(self):
        """Test if positives are recognized"""
        self.paste.body = r"'aws_session_token'\\ssss:\\ssss'AiughaiusDWIHJFUFERHO2134234'"
        self.assertTrue(self.analyzer.match(self.paste))

        self.paste.body = r"'aws'\\ssss:\\ssss'auyhguywgerdbyubduiywebh'"
        self.assertTrue(self.analyzer.match(self.paste))

        self.paste.body = r"'aws_session'\\ssss:\\ssss'YTUF5GUY76ibuihIUIU98jJB+//='"
        self.assertTrue(self.analyzer.match(self.paste))

        self.paste.body = r"'aws_session_token'\\s:\\s'auyhguywgerdbyubduiywebh'"
        self.assertTrue(self.analyzer.match(self.paste))

        self.paste.body = r"'aws_session_token'\\:\\'auyhguywgerdbyubduiywebh'"
        self.assertTrue(self.analyzer.match(self.paste))

        self.paste.body = r"'aws_session_token'\\:\\'auyhguywgerdbyubduiywebh'"
        self.assertTrue(self.analyzer.match(self.paste))

        self.paste.body = r"\\ssssssssssssssssssssss:\\ssssssssssssssss'auyhguywgerdbyubduiywebh'"
        match = self.analyzer.match(self.paste)
        self.assertTrue(match)
        self.assertEqual(r"\\ssssssssssssssssssssss:\\ssssssssssssssss'auyhguywgerdbyubduiywebh'", match[0])

        self.paste.body = r"\\=\\'auyhguywgerdbyubduiywebh'"
        self.assertTrue(self.analyzer.match(self.paste))

        self.paste.body = r"\\=>\\'auyhguywgerdbyubduiywebh'"
        self.assertTrue(self.analyzer.match(self.paste))

    def test_intext(self):
        """Test if matches inside text are recognized"""
        self.paste.body = r"Please always use this session token: \\ssssssssssssssssssssss:\\ssssssssssssssss'auyhguywgerdbyubduiywebh'. Cu soon."
        match = self.analyzer.match(self.paste)
        self.assertTrue(match)
        self.assertEqual(r"\\ssssssssssssssssssssss:\\ssssssssssssssss'auyhguywgerdbyubduiywebh'", match[0])

        self.paste.body = r"Also there are other tokens such as \\=\\'auyhguywgerdbyubduiywebh' which is pretty short"
        match = self.analyzer.match(self.paste)
        self.assertTrue(match)
        self.assertEqual(r"\\=\\'auyhguywgerdbyubduiywebh'", match[0])

    def test_multiple(self):
        """Test if multiple matches are recognized"""
        self.paste.body = r"Please always use this session token: " \
                          r"\\ssssssssssssssssssssss:\\ssssssssssssssss'auyhguywgerdbyubduiywebh'. Also we can use shorter" \
                          r"tokens such as \\=\\'auyhguywgerdbyubduiywebh' which is quite handy."
        match = self.analyzer.match(self.paste)
        self.assertTrue(match)
        self.assertEqual(r"\\ssssssssssssssssssssss:\\ssssssssssssssss'auyhguywgerdbyubduiywebh'", match[0])
        self.assertEqual(r"\\=\\'auyhguywgerdbyubduiywebh'", match[1])

    def test_match_negative(self):
        """Test if negatives are recognized"""
        self.paste.body = "\\ssss:\\ssss'Aiughai'"
        self.assertFalse(self.analyzer.match(self.paste))

        self.paste.body = r"'aws_session'\ssss:\\ssss'YTUF5GUY76ibuihIUIU98jJB+ÒÈÒà'"
        self.assertFalse(self.analyzer.match(self.paste))

        self.paste.body = r"'aws_session_asd'\\aaa:\\ssss'auyhguywgerdbyubduiywebh'"
        self.assertFalse(self.analyzer.match(self.paste))

        self.paste.body = r"\"aws_session\"\\ssss:\ssss'auyhguywgerdbyubduiywebh'"
        self.assertFalse(self.analyzer.match(self.paste))

        self.paste.body = r"'aws_session'\\ssss$\\ssss'auyhguywgerdbyubduiywebh'"
        self.assertFalse(self.analyzer.match(self.paste))

        # We need to use triple strings here - https://stackoverflow.com/questions/27467870/escape-single-quote-in-raw-string-r
        self.paste.body = r"""Any text 'aws_session'\\ssss:\\ssss"auyhguywgerdbyubduiywebh" and more after"""
        self.assertFalse(self.analyzer.match(self.paste))


if __name__ == "__main__":
    unittest.main()
