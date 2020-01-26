# -*- coding: utf-8 -*-
from .regexanalyzer import RegexAnalyzer


class DBConnAnalyzer(RegexAnalyzer):
    """Analyzer to match on email addresses via regex"""
    name = "DBConnAnalyzer"

    def __init__(self, actions):
        # https:// should be ignored
        regex = r"(\b(?!http(?:s)?\b)\w+[a-zA-Z]+:\/\/[a-zA-z0-9.:,\-@]+)"
        super().__init__(actions, regex)
