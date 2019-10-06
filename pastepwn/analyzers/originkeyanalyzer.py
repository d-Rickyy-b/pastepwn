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
        regex = r"^(\w{4}-){4}(\w){4}$"

        super().__init__(action, regex)
