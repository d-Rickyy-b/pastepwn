# -*- coding: utf-8 -*-
import logging

import pymongo
from pymongo.errors import ConnectionFailure

from .abstractdb import AbstractDB


class MongoDB(AbstractDB):

    def __init__(self, ip="127.0.0.1", port=27017, dbname="pastepwn", collectionname="pastes"):
        """
        Initialize mongodb database.

        Args:
            self: (todo): write your description
            ip: (str): write your description
            port: (int): write your description
            dbname: (str): write your description
            collectionname: (str): write your description
        """
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initializing MongoDB - {0}:{1}".format(ip, port))
        self.db = pymongo.MongoClient(ip, port, serverSelectionTimeoutMS=5000)

        try:
            self.db.admin.command("ismaster")
        except ConnectionFailure as e:
            self.logger.error(e)
            raise e

        self.logger.debug("Connected to database!")

        self.db = self.db[dbname]
        self.collection = self.db[collectionname]
        self.collection.create_index([('key', pymongo.ASCENDING)], unique=True)

    def _insert_data(self, data):
        """
        Add data to collection.

        Args:
            self: (todo): write your description
            data: (array): write your description
        """
        self.collection.update_one({'key': data['key']}, {'$set': data}, upsert=True)

    def _get_data(self, key, value):
        """
        Get the value for the given key.

        Args:
            self: (todo): write your description
            key: (str): write your description
            value: (todo): write your description
        """
        return self.collection.find({key: value})

    # TODO def update_data(self, )

    # TODO def delete_data(self,)

    def count(self, key, value):
        """
        Return the number of items in the collection.

        Args:
            self: (todo): write your description
            key: (str): write your description
            value: (todo): write your description
        """
        return self.collection.find({key: value}).count()

    def count_all(self):
        """
        Return all the number of documents

        Args:
            self: (todo): write your description
        """
        return self.collection.count()

    def store(self, paste):
        """
        Stores data into the clipboard

        Args:
            self: (todo): write your description
            paste: (todo): write your description
        """
        self.logger.debug("Storing paste {0}".format(paste.key))

        try:
            self._insert_data(paste.to_dict())
        except pymongo.errors.DuplicateKeyError:
            self.logger.debug("Duplicate key '{0}' - Not storing paste".format(paste.key))

    def get(self, key):
        """
        Returns the value of the key.

        Args:
            self: (todo): write your description
            key: (todo): write your description
        """
        return self._get_data("key", key)
