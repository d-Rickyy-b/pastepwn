# -*- coding: utf-8 -*-

import unittest

from pastepwn import Paste
from pastepwn.util.templatingengine import TemplatingEngine


class TemplatingEngineTest(unittest.TestCase):

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
        analyzer_name = "TestAnalyzer"
        template = "Matched paste '${key}' by analyzer '${analyzer_name}'. URL is: '${full_url}'"
        comparison = "Matched paste '{0}' by analyzer '{1}'. URL is: '{2}'".format(self.p.get("key"), analyzer_name, self.p.get("full_url"))
        result = TemplatingEngine.fill_template(paste=self.paste, analyzer_name=analyzer_name, template_string=template)
        self.assertEqual(comparison, result, msg="Filled template string is not the same as the expected result!")
