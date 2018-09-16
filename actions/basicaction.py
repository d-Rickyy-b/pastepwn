# -*- coding: utf-8 -*-


class BasicAction(object):
    """Base class for actions which can be performed on pastes"""
    name = "BasicAction"

    def __init__(self):
        pass

    def perform(self, paste, analyzer_name=None):
        """Perform the action on the passed paste"""
        raise NotImplementedError
