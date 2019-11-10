# -*- coding: utf-8 -*-
from .regexanalyzer import RegexAnalyzer


class OriginKeyAnalyzer(RegexAnalyzer):
    """Analyzer to match Origin Keys"""

    def __init__(self, action):
        """
        Analyzer to match Origin Keys
        :param action: Single action or list of actions to be executed when a paste matches
        """
        # Tested Regex against https://pastebin.com/vyNANvwM
        regex = r"\b(?<!-)[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}\b(?!-)"

        super().__init__(action, regex)
