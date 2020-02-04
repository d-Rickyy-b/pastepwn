# -*- coding: utf-8 -*-
from .regexanalyzer import RegexAnalyzer


class PrivateKeyAnalyzer(RegexAnalyzer):
    """Analyzer to match private keys beginnigs via regex"""
    name = "PrivateKeyAnalyzer"

    def __init__(self, actions):
        regex = r"[\-]{4,5}(?: )?BEGIN(?: [A-Z0-9]+)? PRIVATE KEY(?: BLOCK)?(?: )?[\-]{4,5}[\s\w\:\"\-\/\+\=]+?[\-]{4,5}(?: )?END(?: [A-Z0-9]+)? " \
                r"PRIVATE KEY( BLOCK)?(?: )?[\-]{4,5}"
        super().__init__(actions, regex)
