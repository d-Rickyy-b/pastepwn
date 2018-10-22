# -*- coding: utf-8 -*-
import logging
import re

from .basicaction import BasicAction
from pastepwn.util import Request


class TelegramAction(BasicAction):
    """Action to send a Telegram message to a certain user or group"""
    name = "TelegramAction"

    def __init__(self, token, receiver, custom_payload=None, template=None):
        super().__init__()
        self.logger = logging.getLogger(__name__)

        if not re.match("[0-9]+:[a-zA-Z0-9\-_]+", token) or token is None:
            raise ValueError("Bot token not correct or None!")

        self.token = token
        self.receiver = receiver
        self.custom_payload = custom_payload
        self.template = template
        # TODO add possibility to send a template message and inject the paste data into the template

    def perform(self, paste, analyzer_name=None):
        """Send a message via a Telegram bot to a specified user, without checking for errors"""
        # if self.template:
        #    text = self.template.format()
        r = Request()
        text = "New paste matched by analyzer '{0}' - Link: {1}".format(analyzer_name, paste.full_url)
        api_url = "https://api.telegram.org/bot{0}/sendMessage?chat_id={1}&text={2}".format(self.token, self.receiver, text)
        r.get(api_url)
