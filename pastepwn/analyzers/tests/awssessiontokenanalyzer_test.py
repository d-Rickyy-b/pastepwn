import unittest
from unittest import mock

from pastepwn.analyzers.awssessiontokenanalyzer import AWSSessionTokenAnalyzer


class TestAWSSessionTokenAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = AWSSessionTokenAnalyzer(None)
        self.paste = mock.Mock()

    def test_mach_positive(self):
        """Test if positives are recognized"""
        self.paste.body = "'aws_session_token'\\\\ssss:\\\\ssss'AiughaiusDWIHJFUFERHO2134234'"
        self.assertTrue(self.analyzer.match(self.paste))

        self.paste.body = "'aws'\\\\ssss:\\\\ssss'auyhguywgerdbyubduiywebh'"
        self.assertTrue(self.analyzer.match(self.paste))

        self.paste.body = "'aws_session'\\\\ssss:\\\\ssss'YTUF5GUY76ibuihIUIU98jJB+//='"
        self.assertTrue(self.analyzer.match(self.paste))

        self.paste.body = "'aws_session_token'\\\\s:\\\\s'auyhguywgerdbyubduiywebh'"
        self.assertTrue(self.analyzer.match(self.paste))

        self.paste.body = "'aws_session_token'\\\\:\\\\'auyhguywgerdbyubduiywebh'"
        self.assertTrue(self.analyzer.match(self.paste))

        self.paste.body = "'aws_session_token'\\\\:\\\\'auyhguywgerdbyubduiywebh'"
        self.assertTrue(self.analyzer.match(self.paste))

        self.paste.body = "\\\\ssssssssssssssssssssss:\\\\ssssssssssssssss'auyhguywgerdbyubduiywebh'"
        self.assertTrue(self.analyzer.match(self.paste))

        self.paste.body = "\\\\=\\\\'auyhguywgerdbyubduiywebh'"
        self.assertTrue(self.analyzer.match(self.paste))

        self.paste.body = "\\\\=>\\\\'auyhguywgerdbyubduiywebh'"
        self.assertTrue(self.analyzer.match(self.paste))

    def test_match_negative(self):
        """Test if negatives are recognized"""
        self.paste.body = "\\\\ssss:\\\\ssss'Aiughai'"
        self.assertFalse(self.analyzer.match(self.paste))

        self.paste.body = "'aws_session'\\ssss:\\\\ssss'YTUF5GUY76ibuihIUIU98jJB+ÒÈÒà'"
        self.assertFalse(self.analyzer.match(self.paste))

        self.paste.body = "'aws_session_asd'\\\\aaa:\\\\ssss'auyhguywgerdbyubduiywebh'"
        self.assertFalse(self.analyzer.match(self.paste))

        self.paste.body = "\"aws_session\"\\\\ssss:\\ssss'auyhguywgerdbyubduiywebh'"
        self.assertFalse(self.analyzer.match(self.paste))

        self.paste.body = "'aws_session'\\\\ssss$\\\\ssss'auyhguywgerdbyubduiywebh'"
        self.assertFalse(self.analyzer.match(self.paste))

        self.paste.body = "'aws_session'\\\\ssss:\\\\ssss\"auyhguywgerdbyubduiywebh\""
        self.assertFalse(self.analyzer.match(self.paste))


if __name__ == '__main__':
    unittest.main()
