# -*- coding: utf-8 -*-
from actions import BasicAction
import os


class SaveFileAction(BasicAction):
    """Action to save a file to the disk"""
    name = "SaveFileAction"

    def __init__(self, path):
        super().__init__()
        self.path = path

    def perform(self, paste):
        with open(os.path.join(self.path), "w") as file:
            file.write(str(paste))
