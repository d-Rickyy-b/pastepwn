# -*- coding: utf-8 -*-
from .regexanalyzer import RegexAnalyzer

_EMAIL_PASSWORD_REGEX = r'[\w\.\+_-]+@[\w\._-]+\.[a-zA-Z]*\:[\w\.\+\!\$\#\^&\*\(\)\{\}\[\]\_\-\@\%\=\§\\\/\'\`\´\?\<\>\;\"\:\|\,\~]+'


class EmailPasswordPairAnalyzer(RegexAnalyzer):
    """Analyzer to match username:password pairs"""
    name = "EmailPasswordPairAnalyzer"

    def __init__(self, actions):
        super().__init__(actions, _EMAIL_PASSWORD_REGEX)
