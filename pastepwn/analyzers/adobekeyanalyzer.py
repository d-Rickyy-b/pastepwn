# -*- coding: utf-8 -*-
from .regexanalyzer import RegexAnalyzer


class AdobeKeyAnalyzer(RegexAnalyzer):
    """Analyzer to match Adobe License Keys"""

    def __init__(self, action):
        """Analyzer to match Adobe License Keys.
        :param action: Single action or list of actions to be executed when a paste matches
        """
        # Tested Regex against https://pastebin.com/fxWBGf8t
        regex = r"\b(?<!-)[0-9]{4}(?:-[0-9]{4}){5}\b(?!-)"

        super().__init__(action, regex)
