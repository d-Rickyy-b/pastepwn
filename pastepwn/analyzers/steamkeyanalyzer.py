# -*- coding: utf-8 -*-
from .regexanalyzer import RegexAnalyzer


class SteamKeyAnalyzer(RegexAnalyzer):
    """Analyzer to match steam keys via regex."""
    name = "SteamKeyAnalyzer"

    def __init__(self, actions):
        """
        The analyzer matches 5-5-5-5-5 and 5-5-5 pattern steam keys
        Lower case keys seem to be forbidden
        :param actions: A single action or a list of actions to be executed on every paste
        """
        regex = r"\b(?<!-)[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}(?:-[A-Z0-9]{5}-[A-Z0-9]{5})?\b(?!-)"
        super().__init__(actions, regex)
