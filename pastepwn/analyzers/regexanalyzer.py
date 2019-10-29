# -*- coding: utf-8 -*-
import re

from .basicanalyzer import BasicAnalyzer


class RegexAnalyzer(BasicAnalyzer):
    """Analyzer to match the content of a paste via regular expressions"""
    name = "RegexAnalyzer"

    def __init__(self, actions, regex, flags=0):
        super().__init__(actions)
        self.regex = re.compile(regex, flags)

    def match(self, paste):
        """Match the content of a paste via regex. Return true if regex matches"""
        if paste is None:
            return False

        paste_content = paste.body or ""
        return self.regex.search(paste_content) is not None
