# -*- coding: utf-8 -*-

from analyzers import BasicAnalyzer


class WordAnalyzer(BasicAnalyzer):
    """Analyzer to match the content of a paste via regular expressions"""
    name = "WordAnalyzer"

    def __init__(self, action, word, case_sensitive=False):
        super().__init__(action)
        self.word = word
        self.case_sensitive = case_sensitive

    def match(self, paste):
        """Check if the specified word is part of the paste text"""
        paste_content = paste.body

        if self.case_sensitive:
            return self.word.lower() in paste_content.lower()
        else:
            return self.word in paste_content
