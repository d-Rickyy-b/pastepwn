# -*- coding: utf-8 -*-
from .regexanalyzer import RegexAnalyzer


class  CreditCardAnalyzer(RegexAnalyzer):
    def __init__(self, action):
        # Regex taken from https://www.regular-expressions.info/creditcard.html
        regex = "^4[0-9]{12}(?:[0-9]{3})?$|^3[47][0-9]{13}$|^(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}$|^3(?:0[0-5]|[68][0-9])[0-9]{11}$|^6(?:011|5[0-9]{2})[0-9]{12}|^(?:2131|1800|35\d{3})\d{11}$"

        super().__init__(action, regex)

