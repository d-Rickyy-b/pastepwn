# -*- coding: utf-8 -*-
from .regexanalyzer import RegexAnalyzer


class StripeApiKeyAnalyzer(RegexAnalyzer):
    """Analyzer to match Stripe API keys"""

    def __init__(self, actions):
        regex = r"(?:r|s)k_(?:live|test)_[0-9a-zA-Z]{24}"
        super().__init__(actions, regex)
