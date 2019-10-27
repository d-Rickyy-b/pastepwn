# -*- coding: utf-8 -*-


class Paste(object):
    """Representation of a paste object used for example by pastebin"""

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
        self.body = ""

    def set_body(self, body):
        """
        Sets the body of the paste
        :param body: String containing the content of the paste
        :return:
        """
        self.body = str(body or "")

    def __str__(self):
        return str(self.to_dict())

    __repr__ = __str__

    def to_dict(self):
        """
        Generates a dict out of the paste
        :return: Paste as dict
        """
        return self.__dict__.copy()
