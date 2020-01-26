# -*- coding: utf-8 -*-
from .regexanalyzer import RegexAnalyzer


class AzureSubscriptionKeyAnalyzer(RegexAnalyzer):
    """
    Analyzer to match Azure subscription key via regex

    Keys are 32 character alphanumeric (lower case)
    """
    name = "AzureSubscriptionKeyAnalyzer"

    def __init__(self, actions):
        # https://docs.microsoft.com/en-us/azure/api-management/api-management-subscriptions
        regex = r"\b[a-f0-9]{32}\b"
        super().__init__(actions, regex)
