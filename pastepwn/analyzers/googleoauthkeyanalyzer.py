# -*- coding: utf-8 -*-
from .regexanalyzer import RegexAnalyzer


class GoogleOAuthKeyAnalyzer(RegexAnalyzer):

    def __init__(self, actions):
        regex = r"[0-9]+-[0-9A-Za-z_]{32}\.apps\.googleusercontent\.com"
        super().__init__(actions, regex)
        
        # prefix string of numbers with length 10
        regex=r"\d{10,0}-[A-Za-z]{3,}\d{3,}[A-Za-z]{3,}\d{3,}\.apps\.googleusercontent\.com"
        super().__init__(actions, regex)
        
        # prefix string of numbers with length 12
        regex=r"\d{12,}+-[0-9A-Za-z_]{32}\.apps\.googleusercontent\.com"
        super().__init__(actions, regex)
