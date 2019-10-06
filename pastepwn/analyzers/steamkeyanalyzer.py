# -*- coding: utf-8 -*-
from .regexanalyzer import RegexAnalyzer


class SteamKeyAnalyzer(RegexAnalyzer):
    """
    Analyzer to match steam keys via regex
    """
    name = "SteamKeyAnalyzer"

    def __init__(self, actions):
        regex = r"\b[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}\b"
        super().__init__(actions, regex)
