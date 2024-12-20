from .logicalbaseanalyzer import LogicalBaseAnalyzer


class AndAnalyzer(LogicalBaseAnalyzer):
    """Meta analyzer which matches a paste if all of the passed analyzers match that paste"""

    name = "AndAnalyzer"

    def match(self, paste):
        """Returns True if all of the passed analyzers matched"""
        if not self.analyzers:
            return False

        return all(analyzer.match(paste) for analyzer in self.analyzers)
