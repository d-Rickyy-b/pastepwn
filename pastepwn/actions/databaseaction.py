# -*- coding: utf-8 -*-
from .basicaction import BasicAction


class DatabaseAction(BasicAction):
    """Action to save a paste to a database"""
    name = "DatabaseAction"

    def __init__(self, database):
        """
        Initialize database

        Args:
            self: (todo): write your description
            database: (str): write your description
        """
        super().__init__()
        self.database = database

    def perform(self, paste, analyzer_name=None, matches=None):
        """Store an incoming paste in the database"""
        self.database.store(paste)
