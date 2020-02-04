# -*- coding: utf-8 -*-
from .regexanalyzer import RegexAnalyzer


class FacebookAccessTokenAnalyzer(RegexAnalyzer):
    """Analyzer to match a Facebook Access Token"""
    name = "FacebookAccessTokenAnalyzer"
    regex = r"EAACEdEose0cBA[0-9A-Za-z]+"

    def __init__(self, actions):
        """
        Analyzer which always matches a paste to perform actions on every paste
        :param actions: A single action or a list of actions to be executed on every paste
        """
        super().__init__(actions, self.regex)
