# -*- coding: utf-8 -*-
from actions.basicaction import BasicAction


class TelegramAction(BasicAction):
    """Action to send a Telegram message to a certain user or group"""
    name = "TelegramAction"

    def __init__(self, token, receiver, custom_payload=None):
        super().__init__()
        if not re.match("[0-9]+:[a-zA-Z0-9\-_]+", token) or token is None:
            raise ValueError("Bot token not correct or None!")
        self.token = token
        self.receiver = receiver
        self.custom_payload = custom_payload

    def perform(self, paste):
        #TODO send telegram message
        pass
