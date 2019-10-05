from .regexanalyzer import RegexAnalyzer

class PhoneNumberAnalyzer(RegexAnalyzer):
    """Analyzer to match Phone Numbers"""

    def __init__(self, action):
        """Analyzer to match international phone numbers"""
        regex = r"^(\+[0-9]+\s*)?(\([0-9]+\))?[\s0-9\-]+[0-9]+$"

        super().__init__(action, regex)
