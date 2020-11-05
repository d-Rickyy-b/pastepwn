# -*- coding: utf-8 -*-
from .regexanalyzer import RegexAnalyzer


class UplayKeyAnalyzer(RegexAnalyzer):
    """
    Analyzer to match uplay keys via regex
    """
    name = "UplayKeyAnalyzer"

    def __init__(self, actions):
        """
        Initialize actions.

        Args:
            self: (todo): write your description
            actions: (todo): write your description
        """
        regex = r"\b(?<!-)[A-Z0-9]{4}\-[A-Z0-9]{4}\-[A-Z0-9]{4}\-[A-Z0-9]{4}\b(?!-)"
        super().__init__(actions, regex)
