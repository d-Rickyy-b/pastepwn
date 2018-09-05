# -*- coding: utf-8 -*-

from analyzers import BasicAnalyzer


class WordAnalyzer(BasicAnalyzer):
    """Analyzer to match the content of a paste via regular expressions"""
    _type = "WordAnalyzer"

    def __init__(self, action, word):
        super().__init__(action)
        self.word = word

    def match(self, paste):
        """Check if the specified word is part of the paste text"""
        paste_content = paste.body
        return self.word in paste_content
