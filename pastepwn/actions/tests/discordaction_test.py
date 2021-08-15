# -*- coding: utf-8 -*-
import logging
import os
import sys
import unittest
from unittest.mock import Mock

from pastepwn import Paste
from pastepwn.actions.discordaction import DiscordAction


@unittest.skipIf(os.getenv("CI"), "running on CI")
class TestDiscordAction(unittest.TestCase):
    def setUp(self):
        """Setup the environment to test the action"""
        pass

    def tearDown(self):
        """Reset the environment to a clean state"""
        pass

    @staticmethod
    def generate_paste():
        """Returns a paste for testing"""
        p = {"scrape_url": "https://scrape.pastebin.com/api_scrape_item.php?i=0CeaNm8Y",
             "full_url": "https://pastebin.com/0CeaNm8Y",
             "date": "1442911802",
             "key": "0CeaNm8Y",
             "size": "890",
             "expire": "1442998159",
             "title": "Once we all know when we goto function",
             "syntax": "java",
             "user": "admin",
             "body": "This is a test for pastepwn"}

        return Paste(p.get("key"), p.get("title"), p.get("user"), p.get("size"), p.get("date"), p.get("expire"), p.get("syntax"), p.get("scrape_url"),
                     p.get("full_url"))

    def test_init(self):
        """Check if initializing the action sets it up correctly"""
        webhook = Mock()
        token = Mock()
        channel_id = Mock()
        template = Mock()

        self.logger = logging.getLogger("pastepwn.actions.discordaction")

        with self.assertLogs(self.logger, level="WARNING") as log:
            # Make sure that the import is not present!
            sys.modules["websockets"] = None
            action = DiscordAction(webhook_url=webhook, token=token, channel_id=channel_id, template=template)
            self.assertEqual(log.output,
                             ["WARNING:pastepwn.actions.discordaction:Could not import 'websockets' module. So you can only use webhooks for discord."])

        self.assertEqual(action.webhook_url, webhook)
        self.assertEqual(action.template, template)
        self.assertFalse(action.bot_available, msg="Websockets are not available. bot_available must be false!")

    def test_init_logging(self):
        """Make sure that the action logs information about missing imports"""
        webhook = Mock()
        token = Mock()
        channel_id = Mock()
        template = Mock()

        self.logger = logging.getLogger("pastepwn.actions.discordaction")

        with self.assertLogs(self.logger, level="WARNING") as log:
            # Make sure that the import is not present, so that we do log!
            sys.modules["websockets"] = None
            action = DiscordAction(webhook_url=webhook, token=token, channel_id=channel_id, template=template)
            self.assertEqual(log.output,
                             ["WARNING:pastepwn.actions.discordaction:Could not import 'websockets' module. So you can only use webhooks for discord."])

        self.assertEqual(action.webhook_url, webhook)
        self.assertEqual(action.template, template)
        self.assertFalse(action.bot_available, msg="Websockets are not available. bot_available must be false!")

    def test_init_import_successful(self):
        """Check if the initialization works fine if the import is successful"""
        webhook = Mock()
        token = Mock()
        channel_id = Mock()
        template = Mock()

        self.logger = logging.getLogger("pastepwn.actions.discordaction")

        # Make sure that the import is present!
        sys.modules["websockets"] = Mock()
        action = DiscordAction(webhook_url=webhook, token=token, channel_id=channel_id, template=template)
        self.assertTrue(action.bot_available, msg="Websockets are available. bot_available must be true!")

        # We are using the webhooks so we don't have the token/channel_id attribute
        self.assertEqual(action.webhook_url, webhook)
        self.assertEqual(action.template, template)

    def test_init_token(self):
        """Check if initializing the action with a token works as expected"""
        token = Mock()
        channel_id = Mock()
        template = Mock()

        sys.modules["websockets"] = Mock()
        action = DiscordAction(webhook_url=None, token=token, channel_id=channel_id, template=template)

        self.assertEqual(action.token, token)
        self.assertEqual(action.channel_id, channel_id)
        self.assertEqual(action.template, template)
        self.assertTrue(action.bot_available)
        self.assertFalse(action.identified)

    def test_init_token_exception(self):
        """Check if initializing the action with a token but without websockets module throws an exception"""
        token = Mock()
        channel_id = Mock()
        template = Mock()

        sys.modules["websockets"] = None
        with self.assertRaises(NotImplementedError, msg="No exception although module could not be imported"):
            # When it's not possible to import the websockets module, we need to throw an exception
            _ = DiscordAction(webhook_url=None, token=token, channel_id=channel_id, template=template)

    def test_init_general_exception(self):
        """Check if an exception occurrs on an error state"""
        with self.assertRaises(ValueError, msg="No error raised, although both token and channel_id are None!"):
            _ = DiscordAction(webhook_url=None, token=None, channel_id=None)

        with self.assertRaises(ValueError, msg="No error raised, although channel_id is None!"):
            _ = DiscordAction(webhook_url=None, token=Mock(), channel_id=None)

        with self.assertRaises(ValueError, msg="No error raised, although token is None!"):
            _ = DiscordAction(webhook_url=None, token=None, channel_id=Mock())


if __name__ == "__main__":
    unittest.main()
