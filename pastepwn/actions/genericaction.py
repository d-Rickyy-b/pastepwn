# -*- coding: utf-8 -*-
from .basicaction import BasicAction


class GenericAction(BasicAction):
    """Action to execute a custom function"""
    name = "GenericAction"

    def __init__(self, func):
        super().__init__()
        self.func = func

    def perform(self, paste, analyzer_name=None):
        self.func(paste)
