# -*- coding: utf-8 -*-
from .logicalbaseanalyzer import LogicalBaseAnalyzer


class OrAnalyzer(LogicalBaseAnalyzer):
    """Meta analyzer which matches a paste if any of the passed analyzers match that paste"""
    name = "OrAnalyzer"

    def match(self, paste):
        """Returns True if all of the passed analyzers matched"""
        for analyzer in self.analyzers:
            if analyzer.match(paste):
                return True

        return False
