# -*- coding: utf-8 -*-
from .regexanalyzer import RegexAnalyzer


class MailChimpApiKeyAnalyzer(RegexAnalyzer):

    def __init__(self, actions):
        """
        Initialize actions.

        Args:
            self: (todo): write your description
            actions: (todo): write your description
        """
        regex = r"[0-9a-f]{32}-us[0-9]{12}"
        super().__init__(actions, regex)
