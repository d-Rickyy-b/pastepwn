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
        if body is None:
            body = ""
        self.body = str(body)

    def __str__(self):
        paste_dict = self.to_dict()
        return str(paste_dict)

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        paste_dict = {'scrape_url': self.scrape_url,
                      'full_url': self.full_url,
                      'date': self.date,
                      'key': self.key,
                      'size': self.size,
                      'expire': self.expire,
                      'title': self.title,
                      'syntax': self.syntax,
                      'user': self.user,
                      'body': self.body}
        return paste_dict
