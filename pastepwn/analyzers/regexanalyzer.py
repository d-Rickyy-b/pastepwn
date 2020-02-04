# -*- coding: utf-8 -*-
import re

from .basicanalyzer import BasicAnalyzer


class RegexAnalyzer(BasicAnalyzer):
    """Analyzer to match the content of a paste via regular expressions"""
    name = "RegexAnalyzer"

    def __init__(self, actions, regex, flags=0):
        super().__init__(actions)
        self.regex = re.compile(regex, flags)

    def verify(self, results):
        """Method to perform additional checks to test if the matches are actually valid"""
        # This method can be overwritten by subclasses in order to perform more checks within the analyzer
        return results

    def match(self, paste):
        """Match the content of a paste via regex. Return true if regex matches"""
        if paste is None:
            return False

        paste_content = paste.body or ""
        matches = self.regex.findall(paste_content)

        return self.verify(matches)
