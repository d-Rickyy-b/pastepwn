# -*- coding: utf-8 -*-
import logging
from string import Template

import twitter

from pastepwn.util import DictWrapper
from .basicaction import BasicAction


class TwitterAction(BasicAction):
    """Action to tweet a message to a given account"""

    name = "TwitterAction"

    def __init__(
        self,
        consumer_key,
        consumer_secret,
        access_token_key,
        access_token_secret,
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

        if template is not None:
            self.template = Template(template)
        else:
            self.template = None

    def perform(self, paste, analyzer_name=None):
        """Tweet a message"""

        if self.template is None:
            text = "New paste matched by analyzer '{0}' - Link: {1}".format(
                analyzer_name, paste.full_url
            )
        else:
            paste_dict = paste.to_dict()
            paste_dict["analyzer_name"] = analyzer_name
            text = self.template.safe_substitute(DictWrapper(paste_dict))

        self.twitter_api.PostUpdate(text)
