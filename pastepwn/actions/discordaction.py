# -*- coding: utf-8 -*-
import logging
import re
import json
import discord
from string import Template

from pastepwn.util import Request, DictWrapper
from .basicaction import BasicAction


class DiscordAction(BasicAction):
    """Action to send a Discord message to a certain channel via a webhook"""
    name = "DiscordAction"

    def __init__(self, webhook, token, channel, custom_payload=None, template=None):
        super().__init__()
        self.logger = logging.getLogger(__name__)

        self.webhook = webhook
        self.token = token
        self.channel = channel
        self.custom_payload = custom_payload
        if template is not None:
            self.template = Template(template)
        else:
            self.template = None

    def perform(self, paste, analyzer_name=None):
        """Send a message via a Discord bot or webhook to a specified channel, without checking for errors"""
        r = Request()
        if self.webhook is None:
            client = discord.Client()

            @client.event
            async def on_ready():
                msg = "New paste matched by analyzer '{0}' - Link: {1}".format(analyzer_name, paste.full_url)
                channel = client.get_channel(self.channel)
                await channel.send(msg)
                await client.close()

            client.run(self.token)
        else:
            if self.template is None:
                text = "New paste matched by analyzer '{0}' - Link: {1}".format(analyzer_name, paste.full_url)
            else:
                paste_dict = paste.to_dict()
                paste_dict["analyzer_name"] = analyzer_name
                text = self.template.safe_substitute(DictWrapper(paste_dict))

            pasteJson = json.dumps( {"content":paste})

            r.post(self.webhook, pasteJson)