# -*- coding: utf-8 -*-
import logging

import pymongo

from database import AbstractDB


class MongoDB(AbstractDB):

    def __init__(self, ip="127.0.0.1", port=27017, dbname="pastepwn", collectionname="pastes"):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.db = pymongo.MongoClient(ip, port)
        self.logger.debug("Initializing MongoDB - {0}:{1}".format(ip, port))
        self.db = self.db[dbname]
        self.collection = self.db[collectionname]

    def _insert_data(self, data):
        self.collection.insert_one(data)

    def _get_data(self, key, value):
        return self.collection.find({key: value})

    # TODO def update_data(self, )

    # TODO def delete_data(self,)

    def count(self, key, value):
        return self.collection.find({key: value}).count()

    def count_all(self):
        return self.collection.count()

    def store(self, paste):
        self._insert_data(paste)
        self.logger.info("Storing paste {0}".format(paste.key))

    def get(self, key):
        return self._get_data("key", key)
