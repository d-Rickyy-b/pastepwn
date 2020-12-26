# -*- coding: utf-8 -*-

import unittest

from pastepwn import Paste
from pastepwn.util.templatingengine import TemplatingEngine


class TestTemplatingEngine(unittest.TestCase):

    def setUp(self):
        """Sets up the test case"""
        p = {"scrape_url": "https://scrape.pastebin.com/api_scrape_item.php?i=0CeaNm8Y",
             "full_url": "https://pastebin.com/0CeaNm8Y",
             "date": "1442911802",
             "key": "0CeaNm8Y",
             "size": "890",
             "expire": "1442998159",
             "title": "Once we all know when we goto function",
             "syntax": "java",
             "user": "admin",
             "body": "This is a test for pastepwn"}

        self.p = p
        self.paste = Paste(p.get("key"),
                           p.get("title"),
                           p.get("user"),
                           p.get("size"),
                           p.get("date"),
                           p.get("expire"),
                           p.get("syntax"),
                           p.get("scrape_url"),
                           p.get("full_url"))

    def test_fill_template(self):
        """Checks if templating engine inserts paste data correctly into the template"""
        analyzer_name = "TestAnalyzer"
        template = "Matched paste '${key}' by analyzer '${analyzer_name}'. URL is: '${full_url}'"
        expected = "Matched paste '{0}' by analyzer '{1}'. URL is: '{2}'".format(self.p.get("key"), analyzer_name, self.p.get("full_url"))
        result = TemplatingEngine.fill_template(paste=self.paste, analyzer_name=analyzer_name, template_string=template)
        self.assertEqual(expected, result, msg="Filled template string is not the same as the expected result!")

    def test_fill_template_matches(self):
        """Checks if templating engine inserts the matches correctly into the template"""
        template = "Matches are: ${matches}"
        expected = "Matches are: +123456789\n+987654321"
        matches = ["+123456789", "+987654321"]
        result = TemplatingEngine.fill_template(paste=self.paste, analyzer_name=None, template_string=template, matches=matches)
        self.assertEqual(expected, result, msg="Filled template string is not the same as the expected result!")

    def test_fill_template_kwarg(self):
        """Checks if templating engine inserts arbitrary data via kwargs into the template"""
        template = "Completely new parameter ${random_param} unrelated to paste data can be ${ins} into this string"
        expected = "Completely new parameter 'pastepwnIsCool' unrelated to paste data can be inserted into this string"

        result = TemplatingEngine.fill_template(paste=self.paste, analyzer_name=None, template_string=template, random_param="'pastepwnIsCool'",
                                                ins="inserted"
                                                )
        self.assertEqual(expected, result, msg="Filled template string is not the same as the expected result!")

    def test_fill_template_missing_param(self):
        """Checks if templating engine correctly handles nonexistent params"""
        template = "The nonexistent parameter ${i_do_not_exist} stays the same!"
        expected = "The nonexistent parameter ${i_do_not_exist} stays the same!"

        result = TemplatingEngine.fill_template(paste=self.paste, analyzer_name=None, template_string=template)
        self.assertEqual(expected, result, msg="Filled template string is not the same as the expected result!")

    if __name__ == "__main__":
        unittest.main()
