# -*- coding: utf-8 -*-
from actions import BasicAction
from util import Request


class WebhookAction(BasicAction):
    """Action to perform a Webhook on a matched paste"""
    name = "WebhookAction"

    def __init__(self, url):
        super().__init__()
        self.url = url

    def perform(self, paste, analyzer_name=None):
        """Trigger the webhook"""
        # TODO - More post options ([custom] body, template, choose between GET/POST etc.)
        r = Request()
        r.post(url=self.url)
