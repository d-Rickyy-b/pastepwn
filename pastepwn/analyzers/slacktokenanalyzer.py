# -*- coding: utf-8 -*-
import re

from .regexanalyzer import RegexAnalyzer


class SlackTokenAnalyzer(RegexAnalyzer):
    """Analyzer to match the content of a paste via regular expressions that look like slack tokens"""
    name = "SlackTokenAnalyzer"

    def __init__(self, actions):
        """
        Analyzer which always matches a paste to perform actions on every paste
        :param actions: A single action or a list of actions to be executed on every paste
        """
        regex = r'(xox[pboa]-[0-9]{12}-[0-9]{12}-[0-9]{12}-[a-z0-9]{32})'
        super().__init__(actions, regex)

