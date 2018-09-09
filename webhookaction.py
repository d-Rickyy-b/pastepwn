# -*- coding: utf-8 -*-
from actions import BasicAction


class WebhookAction(BasicAction):
    """Base class for actions which can be performed on pastes"""
    _type = "WebhookAction"

    def __init__(self):
        super().__init__()

    def perform(self, paste):
        """Trigger the webhook"""
        # TODO Add webhook
        pass
