# -*- coding: utf-8 -*-
import logging

from pastepwn.actions import BasicAction
from pastepwn.errors import InvalidActionError
from pastepwn.util import listify


class BasicAnalyzer(object):
    """Basic analyzer class"""
    name = "BasicAnalyzer"

    def __init__(self, actions, identifier=None):
        """Basic analyzer which is extended to create other analyzer subclasses.
        :param actions: A single action or a list of actions to be executed on every paste
        :param identifier: The name or unique identifier for this specific analyzer
        """
        self.logger = logging.getLogger(__name__)
        self.actions = listify(actions)
        self.identifier = identifier or self.name

        # Check if passed action is an instance of an analyzer and not a class - see #175
        # Raises an error if any action is not an object inheriting from BasicAaction
        for action in self.actions:
            self._check_action(action)

    def add_action(self, action):
        """Adds a new action to the already present actions.
        :param action: New action to add to the present actions
        :return: None
        """
        self._check_action(action)
        self.actions.append(action)

    def match(self, paste, unique_matches=False):
        """Checks if a certain paste is matched by the conditions set for this analyzer.
        :param paste: A Paste object which should be matched
        :param unique_matches: A boolean that specifies if matches should be unique - has currently NO effect on merged analyzers!
        :return: A boolean that indicates if the paste has been matched
        """
        raise NotImplementedError("Your analyzer must implement the match method!")

    @staticmethod
    def unique(matches):
        """Takes a list of matches and returns a list with no duplicates.
        :param matches: A list of matches
        :return: A filtered list of matches retaining order
        """
        return sorted(set(matches), key=matches.index)

    def _check_action(self, action):
        """Check if a passed action is a subclass of BasicAction"""
        if not isinstance(action, BasicAction):
            if isinstance(action, type):
                error_msg = "You passed a class as action for '{}' but an instance of an action was expected!".format(self.identifier)
            else:
                error_msg = "You did not pass an action object - inheriting from BasicAction - to '{}'".format(self.identifier)

            self.logger.error(error_msg)
            raise InvalidActionError(error_msg)

    def __and__(self, other):
        return MergedAnalyzer(self, and_analyzer=other)

    def __or__(self, other):
        return MergedAnalyzer(self, or_analyzer=other)

    def __repr__(self):
        if self.identifier is None:
            self.identifier = self.__class__.__name__
        return self.identifier


class MergedAnalyzer(BasicAnalyzer):
    """Combination class to combine multiple analyzers into a single one.
    Doesn't need to be created manually - use the binary operators (& and |) to combine multiple analyzers.
    """
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
            raise ValueError("Neither and_analyzer nor or_analyzer are set!")

        super().__init__(actions, identifier=identifier)

    def match(self, paste, unique_matches=False):
        """Checks if a certain paste is matched by the conditions set for this analyzer.
        :param paste: A Paste object which should be matched
        :param unique_matches: A boolean that specifies if matches should be unique - has currently NO effect on merged analyzers!
        :return: A boolean that indicates if the paste has been matched
        """
        base_analyzer_match = bool(self._base_analyzer.match(paste))
        if self._and_analyzer:
            return base_analyzer_match and bool(self._and_analyzer.match(paste))
        elif self._or_analyzer:
            return base_analyzer_match or bool(self._or_analyzer.match(paste))
