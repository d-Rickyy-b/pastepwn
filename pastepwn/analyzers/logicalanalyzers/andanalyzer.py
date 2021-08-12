# -*- coding: utf-8 -*-
from .logicalbaseanalyzer import LogicalBaseAnalyzer


class AndAnalyzer(LogicalBaseAnalyzer):
    """Meta analyzer which matches a paste if all of the passed analyzers match that paste"""
    name = "AndAnalyzer"

    def match(self, paste):
        """Returns True if all of the passed analyzers matched"""
        if not self.analyzers:
            return False

        for analyzer in self.analyzers:
            if not analyzer.match(paste):
                return False

        return True
