# -*- coding: utf-8 -*-
from pastepwn.util import Request
from .basicaction import BasicAction


class WebhookAction(BasicAction):
    """Action to perform a Webhook on a matched paste"""
    name = "WebhookAction"

    def __init__(self, url, post_data=None):
        """
        Init method for the WebhookAction
        :param url: string, URL to POST against
        :param post_data: boolean, to decide wheather a paste should be sent in the body
        """
        super().__init__()
        self.url = url
        self.post_data = post_data

    def perform(self, paste, analyzer_name=None):
        """
        Trigger the webhook
        :param paste: The paste passed by the ActionHandler
        :param analyzer_name: The name of the analyzer which matched the paste
        :return: None
        """
        if self.post_data is None:
            paste_dict = None
        else:
            paste_dict = paste.to_dict()

        r = Request()
        r.post(url=self.url, data=paste_dict)
