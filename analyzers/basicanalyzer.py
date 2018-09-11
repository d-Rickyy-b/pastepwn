# -*- coding: utf-8 -*-


class BasicAnalyzer(object):
    """Basic analyzer class"""
    name = "BasicAnalyzer"

    def __init__(self, action):
        self.action = action

    def match(self, paste):
        raise NotImplementedError
