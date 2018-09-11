# -*- coding: utf-8 -*-
from actions.basicaction import BasicAction


class SaveFileAction(BasicAction):
    """Action to save a file to the disk"""
    name = "SaveFileAction"

    def __init__(self, path):
        super().__init__()
        self.path = path

    def perform(self, paste):
        #TODO save paste to disk
        pass
