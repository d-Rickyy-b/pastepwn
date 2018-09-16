# -*- coding: utf-8 -*-
from actions import BasicAction


class WebhookAction(BasicAction):
    """Base class for actions which can be performed on pastes"""
    name = "WebhookAction"

    def __init__(self):
        super().__init__()

    def perform(self, paste, analyzer_name=None):
        """Trigger the webhook"""
        # TODO Add webhook
        pass
