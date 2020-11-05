# -*- coding: utf-8 -*-
from .basicaction import BasicAction


class GenericAction(BasicAction):
    """Action to execute a custom function"""
    name = "GenericAction"

    def __init__(self, func):
        """
        Initialize a function.

        Args:
            self: (todo): write your description
            func: (callable): write your description
        """
        super().__init__()
        self.func = func

    def perform(self, paste, analyzer_name=None, matches=None):
        """
        Perform the given paste.

        Args:
            self: (todo): write your description
            paste: (todo): write your description
            analyzer_name: (str): write your description
            matches: (todo): write your description
        """
        self.func(paste)
