# -*- coding: utf-8 -*-
from .basicanalyzer import BasicAnalyzer


class AlwaysTrueAnalyzer(BasicAnalyzer):
    """Analyzer which always matches a paste to perform actions on every paste"""
    name = "AlwaysTrueAnalyzer"

    def __init__(self, actions):
        """
        Analyzer which always matches a paste to perform actions on every paste
        :param actions: A single action or a list of actions to be executed on every paste
        """
        super().__init__(actions)

    def match(self, paste):
        """Always returns True to match every paste available"""
        return True
