# -*- coding: utf-8 -*-
import re

from .basicanalyzer import BasicAnalyzer


class RegexAnalyzer(BasicAnalyzer):
    """Analyzer to match the content of a paste via regular expressions"""
    name = "RegexAnalyzer"

    def __init__(self, action, regex):
        super().__init__(action)
        self.regex = re.compile(regex)

    def match(self, paste):
        """Match the content of a paste via regex. Return true if regex matches"""
        paste_content = paste.body
        return self.regex.search(paste_content) is not None
