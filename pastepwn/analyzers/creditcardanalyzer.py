# -*- coding: utf-8 -*-
from .regexanalyzer import RegexAnalyzer


class CreditCardAnalyzer(RegexAnalyzer):
    """Analyzer to match Credit Cards"""

    def __init__(self, action):
        """
        Analyzer to match Credit Cards
        :param action: Single action or list of actions to be executed when a paste matches
        """
        # Regex taken from https://www.regular-expressions.info/creditcard.html
        regex = r"\b4[0-9]{12}(?:[0-9]{3})?\b|" \
                r"\b3[47][0-9]{13}\b|" \
                r"\b(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}\b|" \
                r"\b3(?:0[0-5]|[68][0-9])[0-9]{11}\b|" \
                r"\b6(?:011|5[0-9]{2})[0-9]{12}|" \
                r"\b(?:2131|1800|35\d{3})\d{11}\b|" \
                r"\b(?:[0-9]{4}[ -]){3}[0-9]{4}\b|" \
                r"\b(?:[0-9]{4}[ -][0-9]{6}[ -][0-9]{4,5})\b"

        super().__init__(action, regex)
