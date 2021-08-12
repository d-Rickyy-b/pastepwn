# -*- coding: utf-8 -*-
from .regexanalyzer import RegexAnalyzer


class MegaLinkAnalyzer(RegexAnalyzer):
    """Analyzer to match mega links via regex."""
    name = "MegaLinkAnalyzer"

    def __init__(self, actions):
        regex = r"\b(?:https?:\/\/)?mega\.nz\/#F![\w-]{8}(?:![\w-]{22}(?:![\w-]{8})?)?\b"
        super().__init__(actions, regex)
