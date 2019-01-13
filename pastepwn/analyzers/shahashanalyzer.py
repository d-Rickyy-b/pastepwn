# -*- coding: utf-8 -*-
from .regexanalyzer import RegexAnalyzer


class SHAHashAnalyzer(RegexAnalyzer):
    """Analyzer to match SHA password hashes via regex"""
    name = "SHAHashAnalyzer"

    def __init__(self, actions):
        regex = r"[a-f0-9]{40}"
        super().__init__(actions, regex)
