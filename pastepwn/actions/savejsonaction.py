# -*- coding: utf-8 -*-
import json
import os

from .savefileaction import SaveFileAction


class SaveJSONAction(SaveFileAction):
    """Action to save a json formatted file to the disk"""
    name = "SaveJSONAction"

    def __init__(self, path):
        super().__init__(path)

    def perform(self, paste, analyzer_name=None):
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        with open(os.path.join(self.path, "{0}.json".format(paste.key)), "w") as file:
            file.write(json.dumps(paste.to_dict()))
