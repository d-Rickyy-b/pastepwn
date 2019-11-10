# -*- coding: utf-8 -*-
import os

from .basicaction import BasicAction


class SaveFileAction(BasicAction):
    """Action to save a file to the disk"""
    name = "SaveFileAction"

    def __init__(self, path):
        super().__init__()
        self.path = path

    def perform(self, paste, analyzer_name=None):
        """
        Stores the paste as a file
        :param paste: The paste to be stored
        :param analyzer_name: The analyzer
        :return:
        """
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        with open(os.path.join(self.path), "w") as file:
            file.write(str(paste))
