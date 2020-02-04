# -*- coding: utf-8 -*-
from .regexanalyzer import RegexAnalyzer

_EMAIL_PASSWORD_REGEX = r'[\w\.\+_-]+@[\w\._-]+\.[a-zA-Z]*\:[\w\.\+\!\$\#\^&\*\(\)\{\}\[\]\_\-\@\%\=\§\\\/\'\`\´\?\<\>\;\"\:\|\,\~]+'


class EmailPasswordPairAnalyzer(RegexAnalyzer):
    """Analyzer to match username:password pairs"""
    name = "EmailPasswordPairAnalyzer"

    def __init__(self, actions, min_amount=0):
        super().__init__(actions, _EMAIL_PASSWORD_REGEX)
        self.min_amount = min_amount

    def verify(self, results):
        """Method to perform additional checks to test if the matches are actually valid"""
        if len(results) >= self.min_amount:
            return results
        return False
