# -*- coding: utf-8 -*-
import logging

import twitter

from pastepwn.util import TemplatingEngine
from .basicaction import BasicAction


class TwitterAction(BasicAction):
    """Action to tweet a message to a given account"""

    name = "TwitterAction"

    def __init__(
            self,
            consumer_key=None,
            consumer_secret=None,
            access_token_key=None,
            access_token_secret=None,
            template=None,
            ):
        super().__init__()

        self.logger = logging.getLogger(__name__)

        self.twitter_api = twitter.Api(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token_key=access_token_key,
            access_token_secret=access_token_secret,
            )
        self.template = template

    def perform(self, paste, analyzer_name=None, matches=None):
        """Tweet a message"""
        text = TemplatingEngine.fill_template(paste, analyzer_name, template_string=self.template, matches=matches)
        self.twitter_api.PostUpdate(text)
