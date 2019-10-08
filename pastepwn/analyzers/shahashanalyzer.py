# -*- coding: utf-8 -*-
from .regexanalyzer import RegexAnalyzer


class SHAHashAnalyzer(RegexAnalyzer):
    """
    Analyzer to match SHA password hashes via regex

    Matches SHA 1, 224, 256, 384, and 512 hashes.
    """
    name = "SHAHashAnalyzer"

    def __init__(self, actions):
        regex = r"\b(?<!-)([a-f0-9]{40}|[a-f0-9]{56}|[a-f0-9]{64}|[a-f0-9]{96}|[a-f0-9]{128})\b(?!-)"
        super().__init__(actions, regex)
