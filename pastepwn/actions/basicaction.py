# -*- coding: utf-8 -*-


class BasicAction(object):
    """Base class for actions which can be performed on pastes"""
    name = "BasicAction"

    def __init__(self):
        """
        Initialize the object

        Args:
            self: (todo): write your description
        """
        pass

    def perform(self, paste, analyzer_name=None, matches=None):
        """Perform the action on the passed paste"""
        raise NotImplementedError
