# -*- coding: utf-8 -*-


class BasicAnalyzer(object):
    """Basic analyzer class"""
    name = "BasicAnalyzer"

    def __init__(self, actions, identifier=None):
        # The identifier parameter is being used to explicitly identify an analyzer
        if actions is None:
            self.actions = []
        elif isinstance(actions, list):
            self.actions = actions
        else:
            self.actions = [actions]
        self.identifier = identifier or self.name

    def match(self, paste):
        raise NotImplementedError
