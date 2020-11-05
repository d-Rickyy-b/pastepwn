# -*- coding: utf-8 -*-
import logging

from .basicaction import BasicAction


class LogAction(BasicAction):
    """Action to log a paste to console"""
    name = "LogAction"

    def __init__(self):
        """
        Initialize the logger.

        Args:
            self: (todo): write your description
        """
        super().__init__()
        self.logger = logging.getLogger(__name__)

    def perform(self, paste, analyzer_name=None, matches=None):
        """
        Perform the given paste.

        Args:
            self: (todo): write your description
            paste: (todo): write your description
            analyzer_name: (str): write your description
            matches: (todo): write your description
        """
        self.logger.debug("New Paste matched: {0}".format(paste))
