from .logicalbaseanalyzer import LogicalBaseAnalyzer


class OrAnalyzer(LogicalBaseAnalyzer):
    """Meta analyzer which matches a paste if any of the passed analyzers match that paste"""

    name = "OrAnalyzer"

    def match(self, paste):
        """Returns True if all of the passed analyzers matched"""
        return any(analyzer.match(paste) for analyzer in self.analyzers)
