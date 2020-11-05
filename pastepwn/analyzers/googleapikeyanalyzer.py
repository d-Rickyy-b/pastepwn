# -*- coding: utf-8 -*-
from .regexanalyzer import RegexAnalyzer


class GoogleApiKeyAnalyzer(RegexAnalyzer):
    """Analyzer that matches Google API Keys via regex"""

    def __init__(self, actions):
        """
        Initialize actions.

        Args:
            self: (todo): write your description
            actions: (todo): write your description
        """
        # https://cloud.google.com/docs/authentication/api-keys
        regex = r"\bAIza[0-9A-Za-z_-]{35}\b"
        super().__init__(actions, regex)
