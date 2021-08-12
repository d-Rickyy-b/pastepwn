# -*- coding: utf-8 -*-
import re
from .basicanalyzer import BasicAnalyzer
from pastepwn.util import listify


class ExactWordAnalyzer(BasicAnalyzer):
    """Analyzer to match the content of a paste by words"""
    name = "ExactWordAnalyzer"

    def __init__(self, actions, words, blacklist=None, case_sensitive=False):
        super().__init__(actions, "{0} ({1})".format(self.name, words))

        self.words = listify(words)
        self.blacklist = blacklist or []
        self.case_sensitive = case_sensitive

    def _blacklist_word_found(self, text):
        blacklist = self.blacklist

        if not len(blacklist):
            return False

        if not self.case_sensitive:
            text = text.lower()
            blacklist = [word.lower() for word in blacklist]

        return any((self._word_in_text(word, text) for word in blacklist))

    def add_word(self, word):
        """
        Add a word to the analyzer
        :param word: Word to be added
        :return:
        """
        self.words.append(word)

    def match(self, paste):
        """Check if the specified words are part of the paste text"""
        if paste is None:
            return False

        paste_content = paste.body or ""

        if self._blacklist_word_found(paste_content):
            return False

        words = self.words

        if not self.case_sensitive:
            paste_content = paste_content.lower()
            words = [word.lower() for word in words]

        return [word for word in words if self._word_in_text(word, paste_content)]

    def _word_in_text(self, word, text):
        pattern = r"\b{0}\b".format(word)
        return re.search(pattern, text) is not None
