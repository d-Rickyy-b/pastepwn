# -*- coding: utf-8 -*-
from .regexanalyzer import RegexAnalyzer


class SlackWebhookAnalyzer(RegexAnalyzer):
    """Analyzer to match (likely) Slack Webhook URLs"""

    def __init__(self, action):
        """
        Analyzer to match (likely) Slack Webhook URLs
        :param action: Single action or list of actions to be executed when a paste matches
        """
        regex = r"https://hooks.slack.com/services/T[a-zA-Z0-9_]{8}/B[a-zA-Z0-9_]{8}/[a-zA-Z0-9_]{24}"

        super().__init__(action, regex)
