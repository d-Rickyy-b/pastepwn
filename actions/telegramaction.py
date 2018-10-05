# -*- coding: utf-8 -*-
import logging
import re

from actions.basicaction import BasicAction
from util import Request


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
        self.request = Request()
        # TODO add possibility to send a template message and inject the paste data into the template

    def perform(self, paste, analyzer_name=None):
        """Send a message via a Telegram bot to a specified user, without checking for errors"""
        if self.template is None:
            self.template = "New paste matched by analyzer '{analyzer_name}' - Link: {url}"

        Template_args = {"analyzer_name": analyzer_name, "url": paste.full_url}  # move the definition of the
        # dictionary in init and add later the parameters passed into perform?
        text = self.template.format(**Template_args)
        api_url = "https://api.telegram.org/bot{0}/sendMessage?chat_id={1}&text={2}".format(self.token, self.receiver, text)
        self.request.get(api_url)
