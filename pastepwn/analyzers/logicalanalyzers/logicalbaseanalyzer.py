# -*- coding: utf-8 -*-
from pastepwn.analyzers.basicanalyzer import BasicAnalyzer
from pastepwn.util import listify


class LogicalBaseAnalyzer(BasicAnalyzer):
    """Meta analyzer used to combine analyzers via a logical operator"""
    name = "LogicalBaseAnalyzer"

    def __init__(self, actions, analyzers, merge_actions=False):
        """
        Meta analyzer used to combine analyzers via a logical operator
        :param actions: A single action or a list of actions to be executed on every paste
        :param analyzers: A single analyzer or a list of analyzers used to match pastes
        """
        super().__init__(actions)
        self.analyzers = listify(analyzers)

        if not self.analyzers:
            self.logger.warning("You have not specified any analyzers inside '{}'".format(self.name))

        if merge_actions:
            self._merge_actions()

    def _merge_actions(self):
        """
        Merges the actions of the passed analyzers into this meta analyzer
        If merged, the actions will be executed if this meta analyzer matches
        :return: None
        """
        for analyzer in self.analyzers:
            for action in analyzer.actions:
                self.actions.append(action)

    def add_analyzer(self, analyzer):
        """
        Add a new analyzer to the list of analyzers
        :param analyzer: A single analyzer used to match pastes
        :return:
        """
        self.analyzers.append(analyzer)

    def match(self, paste):
        """Must be overridden by the subclasses"""
        raise NotImplementedError("match() function must be overridden in the subclasses!")
