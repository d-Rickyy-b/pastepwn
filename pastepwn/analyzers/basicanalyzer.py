# -*- coding: utf-8 -*-


class BasicAnalyzer(object):
    """Basic analyzer class"""
    name = "BasicAnalyzer"

    def __init__(self, action, identifier=None):
        # The identifier parameter is being used to explicitly identify an analyzer
        self.action = action
        self.identifier = identifier or self.name

    def match(self, paste):
        raise NotImplementedError
