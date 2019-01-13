# -*- coding: utf-8 -*-
from .regexanalyzer import RegexAnalyzer


class MD5HashAnalyzer(RegexAnalyzer):
    """Analyzer to match MD5 password hashes via regex"""
    name = "MD5HashAnalyzer"

    def __init__(self, actions):
        regex = r"[a-f0-9]{32}"
        super().__init__(actions, regex)
