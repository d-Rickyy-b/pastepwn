# -*- coding: utf-8 -*-
from .regexanalyzer import RegexAnalyzer


class AWSSessionTokenAnalyzer(RegexAnalyzer):
    """Analyzer to match AWS Session Token via regex."""
    name = "AWSSessionTokenAnalyzer"

    def __init__(self, actions):
        regex = r"(?:(?:\\\"|'|`)?(?:i?aws)?_?(?:i?session)?_?(?:i?token)?(?:\\\"|'|`)?\\\\s{0,50}(?::|=>|=)\\\\s{0,50}(?:\\\"|'|`)?[A-Za-z0-9/+=]{16,}(?:\\\"|'|`)?)"
        super().__init__(actions, regex)
