# -*- coding: utf-8 -*-
import pathlib

from pastepwn.util import TemplatingEngine
from .basicaction import BasicAction


class SaveFileAction(BasicAction):
    """Action to save each paste as a file named '<pasteID>.txt'"""
    name = "SaveFileAction"

    def __init__(self, path, file_ending=".txt", template=None):
        """
        Action to save each paste as a file named '<pasteID>.txt'
        If you want to store metadata within the file, use template strings
        > https://github.com/d-Rickyy-b/pastepwn/wiki/Templating-in-actions
        :param path: The directory in which the file(s) should be stored
        :param template: A template string describing how the paste variables should be filled in
        """
        super().__init__()
        self.path = pathlib.Path(path)
        self.file_ending = file_ending
        self.template = template or "${body}"

    @staticmethod
    def _remove_prefix(input_string, prefix):
        """Remove a prefix from a certain string (e.g. remove '.' as prefix from '.txt')"""
        if input_string.startswith(prefix):
            return input_string[len(prefix):]
        return input_string

    def get_file_content(self, paste, analyzer_name, matches):
        """Returns the content to be written to the file"""
        return TemplatingEngine.fill_template(paste, analyzer_name, template_string=self.template, matches=matches)

    def perform(self, paste, analyzer_name=None, matches=None):
        """
        Stores the paste as a file
        :param paste: The paste passed by the ActionHandler
        :param analyzer_name: The name of the analyzer which matched the paste
        :param matches: List of matches returned by the analyzer
        :return: None
        """
        if not self.path.exists():
            self.path.mkdir(parents=True, exist_ok=True)

        self.file_ending = self._remove_prefix(self.file_ending, ".")

        if self.file_ending == "":
            file_name = str(paste.key)
        else:
            file_name = "{0}.{1}".format(paste.key, self.file_ending)

        file_path = self.path / file_name
        content = self.get_file_content(paste, analyzer_name, matches)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
