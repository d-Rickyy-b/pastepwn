# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from pastepwn.analyzers.slackwebhookanalyzer import SlackWebhookAnalyzer


class TestSlackWebhookAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = SlackWebhookAnalyzer(None)
        self.paste = mock.Mock()

    def test_match_positive(self):
        """Test if positives are recognized"""
        # slack webhook url (sample)
        self.paste.body = "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX"
        self.assertTrue(self.analyzer.match(self.paste))

        # slack webhook url (manually generated)
        self.paste.body = "https://hooks.slack.com/services/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"
        self.assertTrue(self.analyzer.match(self.paste))

        # slack webhook url (randomly generated)
        self.paste.body = "https://hooks.slack.com/services/TwLj3Aeic/B2RnzBQQp/7JkqKP9XxuqN3WFDn3tUA8NJ"
        self.assertTrue(self.analyzer.match(self.paste))

        # slack webhook url (randomly generated)
        self.paste.body = "https://hooks.slack.com/services/TafdGEj9a/B9BdR2SLM/yJAk3gcguM8YzFEpaPnSvZ4Q"
        self.assertTrue(self.analyzer.match(self.paste))

    def test_intext(self):
        """Test if matches inside text are recognized"""
        self.paste.body = "here is the webhook url: The slack webhook key is " \
                          "https://hooks.slack.com/services/T00000000/B00000000" \
                          "/XXXXXXXXXXXXXXXXXXXXXXXX! how about that!"
        match = self.analyzer.match(self.paste)
        self.assertTrue(match)
        self.assertEqual("https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX", match[0])

    def test_multiple(self):
        """Test if multiple matches are recognized"""
        self.paste.body = "here is the webhook url: The slack webhook key is " \
                          "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX! how about that! and now" \
                          "there is another one https://hooks.slack.com/services/T00000000/B00000000/YYYYYYYYYYYYYYYYYYYYYYYY right here!" \
                          "And an invalid url: https://hooks.slack.com/services/T00000000/B00000000/ZZZZZZZZZZ there!"
        match = self.analyzer.match(self.paste)
        self.assertTrue(match)
        self.assertEqual(2, len(match))
        self.assertEqual("https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX", match[0])
        self.assertEqual("https://hooks.slack.com/services/T00000000/B00000000/YYYYYYYYYYYYYYYYYYYYYYYY", match[1])

    def test_match_negative(self):
        """Test if negatives are not recognized"""
        self.paste.body = ""
        self.assertFalse(self.analyzer.match(self.paste))

        self.paste.body = None
        self.assertFalse(self.analyzer.match(self.paste))

        # Other Slack URL (api docs)
        self.paste.body = "https://api.slack.com/incoming-webhooks"
        self.assertFalse(self.analyzer.match(self.paste))

        # Invalid Character
        self.paste.body = "https://hooks.slack.com/services/T00!00000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX"
        self.assertFalse(self.analyzer.match(self.paste))

        # Invalid Length
        self.paste.body = "https://hooks.slack.com/services/T00000000/B0000000/XXXXXXXXXXXXXXXXXXXXXXXX"
        self.assertFalse(self.analyzer.match(self.paste))

        # Invalid Format (/services/Z... vs /services/T...)
        self.paste.body = "https://hooks.slack.com/services/Z00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX"
        self.assertFalse(self.analyzer.match(self.paste))


if __name__ == "__main__":
    unittest.main()
