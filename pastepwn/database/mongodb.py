import logging

import pymongo
from pymongo.errors import ConnectionFailure

from .abstractdb import AbstractDB


class MongoDB(AbstractDB):
    def __init__(self, ip="127.0.0.1", port=27017, dbname="pastepwn", collectionname="pastes"):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.debug(f"Initializing MongoDB - {ip}:{port}")
        timeout_ms = 5000
        self.db = pymongo.MongoClient(ip, port, serverSelectionTimeoutMS=timeout_ms)

        try:
            self.db.admin.command("ismaster")
        except ConnectionFailure as e:
            self.logger.exception("An exception occurred while initializing the database")
            raise

        self.logger.debug("Connected to database!")

        self.db = self.db[dbname]
        self.collection = self.db[collectionname]
        self.collection.create_index([("key", pymongo.ASCENDING)], unique=True)

    def _insert_data(self, data):
        self.collection.update_one({"key": data["key"]}, {"$set": data}, upsert=True)

    def _get_data(self, key, value):
        return self.collection.find({key: value})

    # TODO def update_data(self, )

    # TODO def delete_data(self,)

    def count(self, key, value):
        return self.collection.find({key: value}).count()

    def count_all(self):
        return self.collection.count()

    def store(self, paste):
        self.logger.debug(f"Storing paste {paste.key}")

        try:
            self._insert_data(paste.to_dict())
        except pymongo.errors.DuplicateKeyError:
            self.logger.debug(f"Duplicate key '{paste.key}' - Not storing paste")

    def get(self, key):
        return self._get_data("key", key)
