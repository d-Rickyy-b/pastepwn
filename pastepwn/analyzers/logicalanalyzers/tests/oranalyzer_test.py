# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from pastepwn.actions.basicaction import BasicAction
from pastepwn.analyzers.logicalanalyzers import OrAnalyzer


class TestOrAnalyzer(unittest.TestCase):
    def setUp(self):
        """
        Sets the mock.

        Args:
            self: (todo): write your description
        """
        self.paste = mock.Mock()
        self.gt = mock.Mock()
        self.gt.match = mock.Mock(return_value=True)

        self.gf = mock.Mock()
        self.gf.match = mock.Mock(return_value=False)

    def test_match_positive(self):
        """
        * match the match *

        Args:
            self: (todo): write your description
        """
        self.paste.body = "Test"
        analyzer = OrAnalyzer(None, [self.gt])
        self.assertTrue(analyzer.match(self.paste))

        analyzer = OrAnalyzer(None, [self.gt, self.gt, self.gt])
        self.assertTrue(analyzer.match(self.paste))

        analyzer = OrAnalyzer([], [self.gf, self.gf])
        self.assertFalse(analyzer.match(self.paste))

        analyzer = OrAnalyzer([], [self.gf, self.gf, self.gf])
        self.assertFalse(analyzer.match(self.paste))

        analyzer = OrAnalyzer([], [self.gf, self.gf, self.gf, self.gt])
        self.assertTrue(analyzer.match(self.paste))

    def test_negative(self):
        """
        Check if the body of the negative.

        Args:
            self: (todo): write your description
        """
        self.paste.body = ""

        analyzer = OrAnalyzer([], None)
        self.assertFalse(analyzer.match(self.paste))

        analyzer = OrAnalyzer([], [])
        self.assertFalse(analyzer.match(self.paste))

    def test_actions_present(self):
        """
        Ensures that the given action is present.

        Args:
            self: (todo): write your description
        """
        action = mock.MagicMock(spec=BasicAction)
        analyzer = OrAnalyzer(action, None)
        self.assertEqual([action], analyzer.actions)

    def test_analyzers_present(self):
        """
        Test if the analysis is present.

        Args:
            self: (todo): write your description
        """
        analyzer = OrAnalyzer(None, self.paste)
        self.assertEqual([self.paste], analyzer.analyzers)


if __name__ == '__main__':
    unittest.main()
