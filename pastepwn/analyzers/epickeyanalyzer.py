# -*- coding: utf-8 -*-
from .regexanalyzer import RegexAnalyzer


class EpicKeyAnalyzer(RegexAnalyzer):
    """Analyzer to match Epic Licensing Keys"""

    def __init__(self, action):
        """
        Analyzer to match Epic Licensing Keys
        :param action: Single action or list of actions to be executed when a paste matches
        """
        # Applied general A-Z or 0-9 based on example provided
        # Regex can be adjusted if certain characters are not valid
        regex = r"\b(?<!-)[A-Z0-9]{5}\-[A-Z0-9]{5}\-[A-Z0-9]{5}\-[A-Z0-9]{5}\b(?!-)"

        super().__init__(action, regex)
