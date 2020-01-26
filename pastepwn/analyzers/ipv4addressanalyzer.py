# -*- coding: utf-8 -*-
from .regexanalyzer import RegexAnalyzer


class IPv4AddressAnalyzer(RegexAnalyzer):
    """Analyzer to match on ip addresses via regex"""
    name = "IPv4AddressAnalyzer"

    def __init__(self, actions):
        regex = r"\b\d{1,3}(?:\.\d{1,3}){3}\b"
        super().__init__(actions, regex)
