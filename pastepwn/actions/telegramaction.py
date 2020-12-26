# -*- coding: utf-8 -*-
import logging
import re

from pastepwn.util import Request, TemplatingEngine
from .basicaction import BasicAction


class TelegramAction(BasicAction):
    """Action to send a Telegram message to a certain user or group/channel"""
    name = "TelegramAction"

    def __init__(self, token, receiver, template=None):
        """Action to send a Telegram message to a certain user or group/channel.
        :param token: The Telegram API token for your bot obtained by @BotFather
        :param receiver: The userID/groupID or channelID of the receiving entity
        :param template: A template string describing how the paste variables should be filled in
        """
        super().__init__()
        self.logger = logging.getLogger(__name__)

        if not re.match(r"[0-9]+:[a-zA-Z0-9\-_]+", token) or token is None:
            raise ValueError("Bot token not correct or None!")

        self.token = token
        self.receiver = receiver
        self.template = template

    def perform(self, paste, analyzer_name=None, matches=None):
        """Send a message via a Telegram bot to a specified user, without checking for errors"""
        r = Request()
        text = TemplatingEngine.fill_template(paste, analyzer_name, template_string=self.template, matches=matches)

        api_url = "https://api.telegram.org/bot{0}/sendMessage?chat_id={1}&text={2}".format(self.token, self.receiver, text)
        r.get(api_url)
