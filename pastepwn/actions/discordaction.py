# -*- coding: utf-8 -*-
import logging
import re
import json
from string import Template

from pastepwn.util import Request, DictWrapper
from .basicaction import BasicAction


class DiscordAction(BasicAction):
    """Action to send a Telegram message to a certain user or group"""
    name = "DiscordAction"

    def __init__(self, webhook, custom_payload=None, template=None):
        super().__init__()
        self.logger = logging.getLogger(__name__)

        self.webhook = webhook
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
        
        pasteJson = json.dumps( {"content":paste})
       
        r.post(self.webhook, pasteJson)
