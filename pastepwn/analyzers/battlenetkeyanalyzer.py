# -*- coding: utf-8 -*-
from .regexanalyzer import RegexAnalyzer


class BattleNetKeyAnalyzer(RegexAnalyzer):
    """Analyzer to match battle.net keys via regex."""
    name = "BattleNetKeyAnalyzer"

    def __init__(self, actions):
        # battle.net activation page shows 4-4-4-4 format, but there are also codes in the 4-4-5-4-4 format which work
        regex = r"\b(?<!-)([A-Z0-9]{4}\-[A-Z0-9]{4}\-[A-Z0-9]{4}\-[A-Z0-9]{4}|[A-Z0-9]{4}\-[A-Z0-9]{4}\-[A-Z0-9]{5}\-[A-Z0-9]{4}\-[A-Z0-9]{4})\b(?!-)"
        super().__init__(actions, regex)
