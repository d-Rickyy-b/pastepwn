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

    def __and__(self, other):
        return MergedAnalyzer(self, and_analyzer=other)

    def __or__(self, other):
        return MergedAnalyzer(self, or_analyzer=other)

    def __repr__(self):
        if self.identifier is None:
            self.identifier = self.__class__.__name__
        return self.identifier


class MergedAnalyzer(BasicAnalyzer):
    """Basic analyzer class"""
    name = "MergedAnalyzer"

    def __init__(self, base_analyzer, and_analyzer=None, or_analyzer=None):
        self._base_analyzer = base_analyzer
        self._and_analyzer = and_analyzer
        self._or_analyzer = or_analyzer

        if self._and_analyzer:
            actions = base_analyzer.actions + self._and_analyzer.actions
            identifier = "({} && {})".format(base_analyzer.identifier, self._and_analyzer)
        elif self._or_analyzer:
            actions = base_analyzer.actions + self._or_analyzer.actions
            identifier = "({} || {})".format(base_analyzer.identifier, self._or_analyzer)
        else:
            actions = []
            identifier = "Broken analyzer"
            self.logger.error("Neither and_analyzer nor or_analyzer are set!")

        super().__init__(actions, identifier=identifier)

    def match(self, paste):
        """
        Checks if a certain paste is matched by the conditions set for this analyzer
        :param paste: A :class:`pastepwn.core.paste` object which should be matched
        :return: :obj:`bool` if the paste has been matched
        """
        if self._and_analyzer:
            return bool(self._base_analyzer.match(paste)) and bool(self._and_analyzer.match(paste))
        elif self._or_analyzer:
            return bool(self._base_analyzer.match(paste)) or bool(self._or_analyzer.match(paste))
