# -*- coding: utf-8 -*-
from .regexanalyzer import RegexAnalyzer


class PrivateKeyAnalyzer(RegexAnalyzer):
    """Analyzer to match private keys beginnigs via regex"""
    name = "PrivateKeyAnalyzer"

    def __init__(self, actions):
        regex = r"\-\-\-\-\-BEGIN( [A-Z]+)? PRIVATE KEY( BLOCK)?\-\-\-\-\-"
        super().__init__(actions, regex)
