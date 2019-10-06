# -*- coding: utf-8 -*-
import logging
import json
from string import Template

from pastepwn.util import Request, DictWrapper
from .basicaction import BasicAction


class DiscordAction(BasicAction):
    """Action to send a Telegram message to a certain user or group"""
    name = "DiscordAction"

    def __init__(self, webhook=None, token=None, channel_id=None, custom_payload=None, template=None):
        super().__init__()
        self.logger = logging.getLogger(__name__)

        self.webhook = webhook
        if webhook is None:
            if token is None or channel_id is None:
                raise ValueError('Invalid arguments: requires either webhook or token+channel_id arguments')
            self.token = token
            self.channel_id = channel_id
        self.custom_payload = custom_payload
        if template is not None:
            self.template = Template(template)
        else:
            self.template = None

    def perform(self, paste, analyzer_name=None):
        """Send a message via a Telegram bot to a specified user, without checking for errors"""
        r = Request()
        if self.template is None:
            text = "New paste matched by analyzer '{0}' - Link: {1}".format(analyzer_name, paste.full_url)
        else:
            paste_dict = paste.to_dict()
            paste_dict["analyzer_name"] = analyzer_name
            text = self.template.safe_substitute(DictWrapper(paste_dict))

        if self.webhook is not None:
            # Send to a webhook (no authentication)
            url = self.webhook
        else:
            # Send through Discord bot API (header-based authentication)
            url = 'https://discordapp.com/api/channels/{0}/messages'.format(self.channel_id)
            r.headers = {'Authorization': 'Bot {}'.format(self.token)}

        r.post(url, {"content": text})
