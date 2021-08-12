# -*- coding: utf-8 -*-
from .regexanalyzer import RegexAnalyzer


class MD5HashAnalyzer(RegexAnalyzer):
    """Analyzer to match MD5 password hashes via regex"""

    name = "MD5HashAnalyzer"

    def __init__(self, actions):
        regex = r"\b(?<!-)[a-f0-9]{32}\b(?!-)"
        super().__init__(actions, regex)
