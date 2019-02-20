# -*- coding: utf-8 -*-
from .urlanalyzer import URLAnalyzer


class PastebinURLAnalyzer(URLAnalyzer):
    """ Analyzer to match Pastebin URLs via regex """
    name = "PastebinURLAnalyzer"

    def __init__(self, actions, resolve=False):
        regex = r"((?:https?:\/\/)?pastebin.com\/\S+)"
        super().__init__(actions, regex, resolve)
