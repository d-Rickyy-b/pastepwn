# -*- coding: utf-8 -*-
from .regexanalyzer import RegexAnalyzer


class AWSAccessKeyAnalyzer(RegexAnalyzer):
    """Analyzer to match AWS Access Key via regex.

    Keys are 20 character alphanumeric /+=
    """
    name = "AWSAccessKeyAnalyzer"

    def __init__(self, actions):
        # https://people.eecs.berkeley.edu/~rohanpadhye/files/key_leaks-msr15.pdf
        regex = r"\b(?:A3T[A-Z0-9]|AKIA|AGPA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}\b"
        super().__init__(actions, regex)
