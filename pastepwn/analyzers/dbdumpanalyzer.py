# -*- coding: utf-8 -*-
from .regexanalyzer import RegexAnalyzer


class DatabaseDumpAnalyzer(RegexAnalyzer):
    """Analyzer to match database dumps."""
    name="DatabaseDumpAnalyzer"
    
    def __init__(self, actions):
        regex=r"([^(`,.')\s]+)"
        super().__init__(actions, regex)
