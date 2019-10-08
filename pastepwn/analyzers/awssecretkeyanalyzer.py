# -*- coding: utf-8 -*-
from .regexanalyzer import RegexAnalyzer


class AWSSecretKeyAnalyzer(RegexAnalyzer):
    """
    Analyzer to match AWS Secret Key via regex

    Keys are 40 character alphanumeric with a few symbols /+=
    """
    name = "AWSSecretKeyAnalyzer"

    def __init__(self, actions):
        regex = r"\b[A-Za-z0-9/+=]{40}\b"
        super().__init__(actions, regex)
