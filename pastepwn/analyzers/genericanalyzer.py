# -*- coding: utf-8 -*-
from .basicanalyzer import BasicAnalyzer


class GenericAnalyzer(BasicAnalyzer):
    """Analyzer to pass a function pointer to, in order to create an analyzer on the fly"""
    name = "GenericAnalyzer"

    def __init__(self, action, match_func):
        super().__init__(action)

        if match_func is None:
            raise ValueError("Function to be called cannot be None")

        self.match_func = match_func

    def match(self, paste):
        """Run the passed function and return its return value"""
        return self.match_func(paste)
