# -*- coding: utf-8 -*-
import logging
import re

from pastepwn.util import Request, TemplatingEngine
from .basicaction import BasicAction


class TelegramAction(BasicAction):
    """Action to send a Telegram message to a certain user or group"""
    name = "TelegramAction"

    def __init__(self, token, receiver, custom_payload=None, template=None):
        super().__init__()
        self.logger = logging.getLogger(__name__)

        if not re.match(r"[0-9]+:[a-zA-Z0-9\-_]+", token) or token is None:
            raise ValueError("Bot token not correct or None!")

        self.token = token
        self.receiver = receiver
        self.custom_payload = custom_payload
        self.template = template

    def perform(self, paste, analyzer_name=None, matches=None):
        """Send a message via a Telegram bot to a specified user, without checking for errors"""
        r = Request()
        text = TemplatingEngine.fill_template(paste, analyzer_name, template_string=self.template)

        api_url = "https://api.telegram.org/bot{0}/sendMessage?chat_id={1}&text={2}".format(self.token, self.receiver, text)
        r.get(api_url)
