# -*- coding: utf-8 -*-
from .basicanalyzer import BasicAnalyzer


class WordAnalyzer(BasicAnalyzer):
    """Analyzer to match the content of a paste via regular expressions"""
    name = "WordAnalyzer"

    def __init__(self, actions, word, blacklist=None, case_sensitive=False):
        super().__init__(actions, "{0} ({1})".format(self.name, word))
        self.word = word
        self.blacklist = blacklist or []
        self.case_sensitive = case_sensitive

    def _blacklist_word_found(self, text):
        if self.case_sensitive:
            text = text.lower()
            self.blacklist = [x.lower() for x in self.blacklist]

        for word in self.blacklist:
            if word in text:
                return True

        return False

    def match(self, paste):
        """Check if the specified word is part of the paste text"""
        paste_content = paste.body

        if self._blacklist_word_found(paste_content):
            return False

        if self.case_sensitive:
            return self.word in paste_content
        else:
            return self.word.lower() in paste_content.lower()
