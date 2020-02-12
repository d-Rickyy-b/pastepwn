# -*- coding: utf-8 -*-
from .regexanalyzer import RegexAnalyzer


class Base64Analyzer(RegexAnalyzer):
    """Analyzer to match base64 encoding via regex"""
    name = "Base64Analyzer"

    def __init__(self, actions, min_len=1):
        regex = r"(?<![A-Za-z0-9+\/=])(?:[A-Za-z0-9+\/]{4})+(?:[A-Za-z0-9+\/]{2}==|[A-Za-z0-9+\/]{3}=)?(?![A-Za-z0-9+\/=])"
        self.min_len = min_len
        super().__init__(actions, regex)

    def verify(self, results):
        """Method to perform additional checks to test if the found strings are of sufficient length"""
        validated_strings = []

        for result in results:
            if len(result) >= self.min_len:
                validated_strings.append(result)

        return validated_strings
