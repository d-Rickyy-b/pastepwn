# -*- coding: utf-8 -*-
from actions import SaveFileAction
import os
import json


class SaveJSONAction(SaveFileAction):
    """Action to save a json formatted file to the disk"""
    name = "SaveJSONAction"

    def __init__(self, path):
        super().__init__(path)

    def perform(self, paste):
        with open(os.path.join(self.path, "{0}.json".format(paste.key)), "w") as file:
            file.write(json.dumps(paste.to_dict()))
