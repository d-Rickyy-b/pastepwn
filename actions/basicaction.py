# -*- coding: utf-8 -*-


class BasicAction(object):
    """Base class for actions which can be performed on pastes"""
    _type = "BasicAction"

    def __init__(self):
        pass

    def perform(self, paste):
        """Perform the action on the passed paste"""
        raise NotImplementedError
