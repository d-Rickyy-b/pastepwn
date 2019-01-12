# -*- coding: utf-8 -*-
import logging

from .basicanalyzer import BasicAnalyzer


class GenericAnalyzer(BasicAnalyzer):
    """Analyzer to pass a function pointer to, in order to create an analyzer on the fly"""
    name = "GenericAnalyzer"

    def __init__(self, actions, match_func):
        super().__init__(actions)

        if match_func is None:
            raise ValueError("Function to be called cannot be None")

        self.match_func = match_func

    def match(self, paste):
        """Run the passed function and return its return value"""
        try:
            result = self.match_func(paste)
        except Exception as e:
            result = False
            logging.getLogger(__name__).warning("Executing custom match function raised an exception! {}".format(e))

        return result
