# -*- coding: utf-8 -*-
from .regexanalyzer import RegexAnalyzer


class GoogleApiKeyAnalyzer(RegexAnalyzer):
    """Analyzer that matches Google API Keys via regex"""

    def __init__(self, actions):
        # https://cloud.google.com/docs/authentication/api-keys
        regex = r"\bAIza[0-9A-Za-z_-]{35}\b"
        super().__init__(actions, regex)
