# -*- coding: utf-8 -*-
import json
import os

from .savefileaction import SaveFileAction


class SaveJSONAction(SaveFileAction):
    """Action to save a json formatted file to the disk"""
    name = "SaveJSONAction"

    def __init__(self, path):
        """
        Initialize the specified path.

        Args:
            self: (todo): write your description
            path: (str): write your description
        """
        super().__init__(path)

    def perform(self, paste, analyzer_name=None, matches=None):
        """
        Store the paste in a json file
        :param paste: The paste to be stored
        :param analyzer_name: The analyzer that matched
        :param matches: List of matches returned by the analyzer
        :return: None
        """
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        with open(os.path.join(self.path, "{0}.json".format(paste.key)), "w") as file:
            file.write(json.dumps(paste.to_dict()))
