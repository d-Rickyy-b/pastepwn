import logging
import os

import slack

from string import Template

from pastepwn.util import DictWrapper
from .basicaction import BasicAction



class SlackAction(BasicAction):
    """Action to send a Slack message to a channel"""

    name="SlackAction"

    def __init__(self, token, client, channel_name, template=None):
        super().__init__()
        self.logger = logging.getLogger(__name__)

        if token is None or channel_name is None:
            raise ValueError("Token or Channel Name is either missing or None!")
        
        self.channel_name=channel_name
        self.client=slack.WebClient(token=token) 
        # self.client=slac.WebClient(token=os.environ['SLACK_API_TOKEN'])

        if template is not None:
            self.template = Template(template)
        else:
            self.template = None

    def perform(self, paste, analyzer_name):
        """Send a message to a specified Slack channel without post-assertion"""

        if self.template is None:
            text = "New paste matched by analyzer '{0}' - Link: {1}".format(analyzer_name, paste.full_url)
        else:
            paste_dict = paste.to_dict()
            paste_dict["analyzer_name"] = analyzer_name
            text = self.template.safe_substitute(DictWrapper(paste_dict))
        
        self.client.chat_postMessage(channel=self.channel_name, text=text)