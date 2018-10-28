# -*- coding: utf-8 -*-

import unittest

from pastepwn import Paste


class PasteTest(unittest.TestCase):

    def setUp(self):
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

    def tearDown(self):
        pass

    def test_init_paste(self):
        self.assertEqual(self.p.get("key"), self.paste.key)
        self.assertEqual(self.p.get("title"), self.paste.title)
        self.assertEqual(self.p.get("user"), self.paste.user)
        self.assertEqual(self.p.get("size"), self.paste.size)
        self.assertEqual(self.p.get("date"), self.paste.date)
        self.assertEqual(self.p.get("expire"), self.paste.expire)
        self.assertEqual(self.p.get("syntax"), self.paste.syntax)
        self.assertEqual(self.p.get("scrape_url"), self.paste.scrape_url)
        self.assertEqual(self.p.get("full_url"), self.paste.full_url)
        self.assertEqual(None, self.paste.body)

    def test_set_body(self):
        my_body = "This is a test for pastepwn"
        self.paste.set_body(my_body)
        self.assertEqual(my_body, self.paste.body)

    def test_to_dict(self):
        my_body = "This is a test for pastepwn"
        self.paste.set_body(my_body)

        paste_dict = self.paste.to_dict()
        self.assertEqual(self.p, paste_dict)
