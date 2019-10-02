# -*- coding: utf-8 -*-
from .regexanalyzer import RegexAnalyzer


class DBConnAnalyser(RegexAnalyzer):
    """Analyzer to match on email addresses via regex"""
    name = "DBConnAnalyser"

    def __init__(self, actions):
        # https:// should be ignored
        regex = r"(\b(?!https\b)\w+[a-zA-Z]+://[a-zA-z0-9.:,]+)"
        super().__init__(actions, regex)
