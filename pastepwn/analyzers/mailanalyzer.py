# -*- coding: utf-8 -*-
from .regexanalyzer import RegexAnalyzer


class MailAnalyzer(RegexAnalyzer):
    """Analyzer to match on email addresses via regex"""
    name = "MailAnalyzer"
    pattern = r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"

    def __init__(self, actions):
        # Regex taken from http://emailregex.com/
        super().__init__(actions, self.pattern)
