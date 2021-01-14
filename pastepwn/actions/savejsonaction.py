# -*- coding: utf-8 -*-
import json

from .savefileaction import SaveFileAction


class SaveJSONAction(SaveFileAction):
    """Action to save a json formatted file to the disk"""
    name = "SaveJSONAction"

    def __init__(self, path):
        super().__init__(path, file_ending=".json")

    def get_file_content(self, paste, analyzer_name, matches):
        """Returns the content to be written to the file"""
        return json.dumps(paste.to_dict())
