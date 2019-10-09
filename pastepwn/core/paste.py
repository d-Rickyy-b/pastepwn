# -*- coding: utf-8 -*-


class Paste(object):

    def __init__(self, key, title, user, size, date, expire, syntax, scrape_url, full_url):
        self.key = key
        self.title = title
        self.user = user
        self.size = size
        self.date = date
        self.expire = expire
        self.syntax = syntax
        self.scrape_url = scrape_url
        self.full_url = full_url
        self.body = None

    def set_body(self, body):
        self.body = str(body or "")

    def __str__(self):
        return str(self.to_dict())

    __repr__ = __str__

    def to_dict(self):
        return self.__dict__.copy()
