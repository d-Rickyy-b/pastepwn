import pymongo
import logging


class Database:

    def __init__(self, ip="127.0.0.1", port=27017, dbname="pastepwn", collectionname="pastes"):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Database init")
        self.db = pymongo.MongoClient(ip, port)
        self.db = self.db[dbname]
        self.collection = self.db[collectionname]

    def insert_data(self, dict):
        self.collection.insert_one(dict)

    # TODO return key
    def get_data(self, key, value):
        return self.collection.find({key: value})

    # TODO def update_data(self, )

    # TODO def delete_data(self,)

    def count(self, key, value):
        return self.collection.find({key : value}).count()

    def countAll(self):
        return self.collection.count()



