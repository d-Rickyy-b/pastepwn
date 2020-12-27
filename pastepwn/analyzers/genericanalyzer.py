# -*- coding: utf-8 -*-
import logging

from .basicanalyzer import BasicAnalyzer


class GenericAnalyzer(BasicAnalyzer):
    """Analyzer to pass a function pointer to, in order to create an analyzer on the fly"""
    name = "GenericAnalyzer"

    def __init__(self, actions, match_func, verify_func=None):
        super().__init__(actions)

        if match_func is None:
            raise ValueError("Function to be called cannot be None")
        elif not callable(match_func):
            raise ValueError("Function you provided isn't callable")

        if verify_func is not None and not callable(verify_func):
            raise ValueError("Verify function you provided isn't callable")

        self.verify_func = verify_func
        self.match_func = match_func

    def verify(self, results):
        """Method to perform additional checks to test if the matches are actually valid"""
        # If no custom verify method is specified, we return True
        if self.verify_func is None:
            return results

        # Otherwise we try to execute the verify method
        try:
            return self.verify_func(results)
        except Exception as e:
            logging.getLogger(__name__).warning("Executing custom verify function '{}' raised an exception! {}".format(self.verify_func.__name__, e))

    def match(self, paste):
        """Run the passed function and return its return value"""
        try:
            results = self.match_func(paste)
        except Exception as e:
            logging.getLogger(__name__).warning("Executing custom match function '{}' raised an exception! {}".format(self.match_func.__name__, e))
            return False

        if not self.verify(results):
            return False

        return results
