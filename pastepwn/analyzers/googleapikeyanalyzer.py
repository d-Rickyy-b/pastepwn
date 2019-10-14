# -*- coding: utf-8 -*-
from .regexanalyzer import RegexAnalyzer


class GoogleApiKeyAnalyzer(RegexAnalyzer):

    def __init__(self, actions):
        # https://cloud.google.com/docs/authentication/api-keys
        regex = r"^AIza[0-9A-Za-z_-]{35}$"
        super().__init__(actions, regex)
