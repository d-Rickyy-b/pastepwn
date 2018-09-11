# -*- coding: utf-8 -*-
from actions.basicaction import BasicAction
import re
import logging
from util import Request


class TelegramAction(BasicAction):
    """Action to send a Telegram message to a certain user or group"""
    name = "TelegramAction"

    def __init__(self, token, receiver, custom_payload=None):
        super().__init__()
        self.logger = logging.getLogger(__name__)

        if not re.match("[0-9]+:[a-zA-Z0-9\-_]+", token) or token is None:
            raise ValueError("Bot token not correct or None!")

        self.token = token
        self.receiver = receiver
        self.custom_payload = custom_payload
        self.request = Request()
        # TODO add possibility to send a template message and inject the paste data into the template

    def perform(self, paste):
        """Send a message via a Telegram bot to a specified user, without checking for errors"""
        api_url = "https://api.telegram.org/bot{0}/sendMessage?chat_id={1}".format(self.token, self.receiver)
        self.request.get(api_url)
