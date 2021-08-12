# -*- coding: utf-8 -*-
import re

from .basicanalyzer import BasicAnalyzer


class PasteTitleAnalyzer(BasicAnalyzer):
    """Analyzer to match Paste titles via regex"""

    name = "PasteTitleAnalyzer"

    def __init__(self, actions, regex, flags=0, blacklist=None):
        super().__init__(actions, self.name)
        self.regex = re.compile(regex, flags)
        self.blacklist = blacklist or []

    def match(self, paste):
        """Match the title of a paste via regex. Return true if regex matches"""
        paste_title = paste.title or ""
        return self.regex.findall(paste_title)
