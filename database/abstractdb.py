# -*- coding: utf-8 -*-


class AbstractDB(object):

    def __init__(self):
        pass

    def store(self, paste):
        """Stores a paste in the database"""
        raise NotImplementedError

    def get(self, key):
        """Fetches a paste from the database"""
        raise NotImplementedError
