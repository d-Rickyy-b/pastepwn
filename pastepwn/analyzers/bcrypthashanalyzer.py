# -*- coding: utf-8 -*-
from .regexanalyzer import RegexAnalyzer


class BcryptHashAnalyzer(RegexAnalyzer):
    """Analyzer to match bcrypt password hashes via regex"""
    name = "BcryptHashAnalyzer"

    def __init__(self, actions):
        regex = r"\$2[ayb]\$[\d]{2}\$[./A-Za-z0-9]{53}"
        super().__init__(actions, regex)
