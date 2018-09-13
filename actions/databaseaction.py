# -*- coding: utf-8 -*-
from actions.basicaction import BasicAction


class DatabaseAction(BasicAction):
    """Action to save a paste to a database"""
    name = "DatabaseAction"

    def __init__(self, database):
        super().__init__()
        self.database = database

    def perform(self, paste):
        self.database.store(paste)
