# -*- coding: utf-8 -*-
import logging

from pastepwn.util import listify


class BasicAnalyzer(object):
    """Basic analyzer class"""
    name = "BasicAnalyzer"

    def __init__(self, actions, identifier=None):
        """
        Basic analyzer which is extended to create other analyzer subclasses
        :param actions: A single action or a list of actions to be executed on every paste
        :param identifier: The name or unique identifier for this specific analyzer
        """
        self.actions = listify(actions)
        self.identifier = identifier or self.name
        self.logger = logging.getLogger(self.name)

    def add_action(self, action):
        """
        Adds a new action to the already present actions
        :param action: New action to add to the present actions
        :return: None
        """
        self.actions.append(action)

    def match(self, paste):
        """
        Checks if a certain paste is matched by the conditions set for this analyzer
        :param paste: A :class:`pastepwn.core.paste` object which should be matched
        :return: :obj:`bool` if the paste has been matched
        """
        raise NotImplementedError("Your analyzer must implement the match method!")

    def __repr__(self):
        if self.identifier is None:
            self.identifier = self.__class__.__name__
        return self.identifier
