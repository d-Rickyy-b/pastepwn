# -*- coding: utf-8 -*-
from .mailanalyzer import MailAnalyzer
from .regexanalyzer import RegexAnalyzer


class MailPasswordAnalyzer(RegexAnalyzer):
    """
    Analyzer to match an email and password pair.
    """

    name = "EmailPasswordAnalyzer"

    def __init__(self, actions):
        regex = MailAnalyzer.pattern + ":(.*)"
        super().__init__(actions, regex)
