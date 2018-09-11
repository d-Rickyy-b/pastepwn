# -*- coding: utf-8 -*-
from actions.basicaction import BasicAction


class TelegramAction(BasicAction):
    """Action to send a Telegram message to a certain user or group"""
    name = "TelegramAction"

    def __init__(self, token, receiver, custom_payload=None):
        super().__init__()
        self.token = token
        self.receiver = receiver
        self.custom_payload = custom_payload

    def perform(self, paste):
        #TODO send telegram message
        pass
