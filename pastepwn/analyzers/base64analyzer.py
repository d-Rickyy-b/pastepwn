# -*- coding: utf-8 -*-
from .regexanalyzer import RegexAnalyzer


class Base64Analyzer(RegexAnalyzer):
    """Analyzer to match base64 encoding via regex"""
    name = "Base64Analyzer"

    def __init__(self, actions):
        regex = r"^(?:[A-Za-z0-9+\/]{4})+(?:[A-Za-z0-9+\/]{2}==|[A-Za-z0-9+\/]{3}=)?$"
        super().__init__(actions, regex)
