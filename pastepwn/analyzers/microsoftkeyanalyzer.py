# -*- coding: utf-8 -*-
from .regexanalyzer import RegexAnalyzer


class MicrosoftKeyAnalyzer(RegexAnalyzer):
    """Analyzer to match Microsoft Licensing Keys"""

    def __init__(self, action):
        """
        Analyzer to match Microsoft Licensing Keys
        :param action: Single action or list of actions to be executed when a paste matches
        """
        # Tested Regex against https://pastebin.com/r3QdpFJf
        regex = r"\b(?<!-)[2346789BCDFGHJKMNPQRTVWXY]{5}(?:-[2346789BCDFGHJKMNPQRTVWXY]{5}){4}\b(?!-)"

        super().__init__(action, regex)
