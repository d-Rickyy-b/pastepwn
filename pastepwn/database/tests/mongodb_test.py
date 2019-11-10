# -*- coding: utf-8 -*-

import os
import random
import string
import unittest

from pastepwn import Paste
from pastepwn.database import MongoDB


@unittest.skipIf("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true", "Skipping this test on Travis CI.")
class MongoDBTest(unittest.TestCase):

    def setUp(self):
        rand_text = list()
        for i in range(3):
            rand_text.append(''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8)))

        p = {"scrape_url": "https://scrape.pastebin.com/api_scrape_item.php?i=" + rand_text[0],
             "full_url": "https://pastebin.com/" + rand_text[0],
             "date": "1442911802",
             "key": rand_text[0],
             "size": "890",
             "expire": "1442998159",
             "title": "Once we all know when we goto function",
             "syntax": "java",
             "user": "admin",
             "body": rand_text[1:],
             }

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

        self.database = MongoDB(collectionname="pastepwn_test")

    def tearDown(self):
        self.database.db.drop_collection("pastepwn_test")

    def test_insert_same_key(self):
        for body_text in self.p['body']:
            self.paste.set_body(body_text)
            self.database.store(self.paste)

        self.assertEqual(self.database.get(self.p['key']).next()['body'], self.p['body'][1])
