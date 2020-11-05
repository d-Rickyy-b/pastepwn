# -*- coding: utf-8 -*-


class AbstractDB(object):

    def __init__(self):
        """
        Initialize the object

        Args:
            self: (todo): write your description
        """
        pass

    def store(self, paste):
        """Stores a paste in the database"""
        raise NotImplementedError

    def get(self, key):
        """Fetches a paste from the database"""
        raise NotImplementedError
