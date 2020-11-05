# -*- coding: utf-8 -*-
from .basicanalyzer import BasicAnalyzer


class WordAnalyzer(BasicAnalyzer):
    """Analyzer to match the content of a paste by words"""
    name = "WordAnalyzer"

    def __init__(self, actions, words, blacklist=None, case_sensitive=False):
        """
        Initialize the list.

        Args:
            self: (todo): write your description
            actions: (todo): write your description
            words: (todo): write your description
            blacklist: (todo): write your description
            case_sensitive: (bool): write your description
        """
        super().__init__(actions, "{0} ({1})".format(self.name, words))

        if words is None:
            self.words = []
        elif isinstance(words, list):
            self.words = words
        else:
            self.words = [words]

        self.blacklist = blacklist or []
        self.case_sensitive = case_sensitive

    def _blacklist_word_found(self, text):
        """
        Return true if text contains blacklist.

        Args:
            self: (todo): write your description
            text: (str): write your description
        """
        if not self.case_sensitive:
            text = text.lower()
            self.blacklist = [x.lower() for x in self.blacklist]

        for word in self.blacklist:
            if word in text:
                return True

        return False

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

        _matches = []
        if self.case_sensitive:
            for word in self.words:
                # Never use 'return word in paste_content' - otherwise you will
                # return false before all words have been checked
                if word in paste_content:
                    _matches.append(word)
        else:
            for word in self.words:
                if word.lower() in paste_content.lower():
                    _matches.append(word)

        return _matches
