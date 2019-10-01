# -*- coding: utf-8 -*-
from .basicanalyzer import BasicAnalyzer


class DatabaseDumpAnalyzer(BasicAnalyzer):
    """Analyzer to match database dump"""
    name = "DatabaseDumpAnalyzer"

    def __init__(self, actions):
        """
        Analyzer to match database dump
        :param actions: A single action or a list of actions to be executed on every paste
        """
        # This regex match the columns of a database
        regex = r"[(]((`\w+`|\d), )+(`\w+`|\d)[)]"
        
        super().__init__(actions, regex)
