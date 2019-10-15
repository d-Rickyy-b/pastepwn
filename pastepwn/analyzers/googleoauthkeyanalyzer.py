# -*- coding: utf-8 -*-
from .regexanalyzer import RegexAnalyzer


class GoogleOAuthKeyAnalyzer(RegexAnalyzer):

    def __init__(self, actions):
        regex = r"[0-9]+-[0-9A-Za-z_]{32}\.apps\.googleusercontent\.com"
        super().__init__(actions, regex)
