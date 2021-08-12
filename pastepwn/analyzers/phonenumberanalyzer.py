# -*- coding: utf-8 -*-
from .regexanalyzer import RegexAnalyzer


class PhoneNumberAnalyzer(RegexAnalyzer):
    """Analyzer to match Phone Numbers"""

    def __init__(self, action):
        """Analyzer to match international phone numbers"""
        # from stackoverflow: https://stackoverflow.com/questions/2113908/what-regular-expression-will-match-valid-international-phone-numbers
        regex = r"\+(?:9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|2[98654321]\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|4[987654310]|3[" \
                r"9643210]|2[70]|7|1)[\d \-\(\)]{2,16}(?!\d)"

        super().__init__(action, regex)

    def verify(self, results):
        """Verify possible phone numbers"""
        # Currently we don't really do verifications - we only replace spaces in the end,
        # because our regex also matches whitespace in the end
        return [result.rstrip() for result in results]
