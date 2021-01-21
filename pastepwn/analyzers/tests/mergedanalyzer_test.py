# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from pastepwn.analyzers.basicanalyzer import BasicAnalyzer
from pastepwn.analyzers.basicanalyzer import MergedAnalyzer


class TestMergedAnalyzer(unittest.TestCase):
    class NewAnalyzer(BasicAnalyzer):
        """Test Analyzer for testing mergedAnalyzer"""

        def __init__(self, return_value):
            super().__init__(actions=None)
            self.return_value = return_value

        def match(self, paste):
            """Match func"""
            return self.return_value

    def setUp(self):
        """Setup test case"""
        self.true_analyzer = self.NewAnalyzer(True)
        self.false_analyzer = self.NewAnalyzer(False)
        self.paste_mock = mock.Mock()
        self.paste_mock.body = "This is a mock paste"

    def test_and(self):
        """Check if logical and between analyzers works fine"""
        and_analyzer = self.true_analyzer & self.false_analyzer

        # One analyzer returns False, the other True, this should evaluate to False
        self.assertFalse(and_analyzer.match(self.paste_mock))

        and_analyzer2 = self.true_analyzer & self.true_analyzer
        # Since both analyzers return true, this should now return True as well
        self.assertTrue(and_analyzer2.match(self.paste_mock))

    def test_or(self):
        """Check if logical or between analyzers works fine"""
        # One analyzer returns False, the other True, this should evaluate to True
        or_analyzer = self.true_analyzer | self.false_analyzer
        self.assertTrue(or_analyzer.match(self.paste_mock))

        # Since both return true, this should return True as well
        or_analyzer2 = self.true_analyzer | self.false_analyzer
        self.assertTrue(or_analyzer2.match(self.paste_mock))

        or_analyzer3 = self.false_analyzer | self.true_analyzer
        self.assertTrue(or_analyzer3.match(self.paste_mock))

    def test_both(self):
        """Check if logical and/or both work fine in combination with each other"""
        # One analyzer returns False, the other True, this should evaluate to False
        and_analyzer = self.true_analyzer & self.false_analyzer
        self.assertFalse(and_analyzer.match(self.paste_mock))

        # Since both return true, this should return True as well
        or_analyzer = self.true_analyzer | self.false_analyzer
        self.assertTrue(or_analyzer.match(self.paste_mock))

    def test_none(self):
        """Check that error is raised in case no value is given for and/or/not_analyzer"""
        with self.assertRaises(ValueError):
            MergedAnalyzer(base_analyzer=None)

    def test_long_chain(self):
        """Check if logical and/or both work fine in long combinations with each other"""
        # Long chain of true_analyzers must evaluate to True
        and_analyzer = self.true_analyzer & self.true_analyzer & self.true_analyzer & self.true_analyzer & \
            self.true_analyzer & self.true_analyzer & self.true_analyzer & self.true_analyzer
        self.assertTrue(and_analyzer.match(self.paste_mock))

        # A single false_analyzer must make the term evaluate to false
        and_analyzer2 = self.true_analyzer & self.true_analyzer & self.true_analyzer & self.false_analyzer & \
            self.true_analyzer & self.true_analyzer & self.true_analyzer & self.true_analyzer
        self.assertFalse(and_analyzer2.match(self.paste_mock))

        # Since one returns true, this should return True as well
        or_analyzer = self.false_analyzer | self.false_analyzer | self.false_analyzer | self.false_analyzer | \
            self.false_analyzer | self.true_analyzer | self.true_analyzer | self.true_analyzer
        self.assertTrue(or_analyzer.match(self.paste_mock))

    def test_list_and(self):
        """Check if other return values than booleans are handled correctly with logical and"""
        and_analyzer = self.NewAnalyzer(["Test", 123]) & self.NewAnalyzer([])
        res = and_analyzer.match(self.paste_mock)
        self.assertIsInstance(res, bool)
        self.assertFalse(res)

    def test_list_or(self):
        """Check if other return values than booleans are handled correctly with logical or"""
        and_analyzer = self.NewAnalyzer(["Test", 123]) | self.NewAnalyzer([])
        res = and_analyzer.match(self.paste_mock)
        self.assertIsInstance(res, bool)
        self.assertTrue(res)


if __name__ == "__main__":
    unittest.main()
