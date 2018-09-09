import pymongo

class Database:

    def __init__(self, ip="127.0.0.1", port=27017, dbname="pastepwn", collectionname="pastes"):
        print("Database init")
        self.db = pymongo.MongoClient(ip, port)
        self.db = self.db[dbname]
        self.collection = self.db[collectionname]
        self.logger = logging.getLogger(__name__)


    def insertData(self, dict):
        self.collection.insert_one(dict)

    #ToDo return key
    def getData(self, key, value):
        return self.collection.find({key: value})

    #ToDo def updateData(self, )

    def count(self, key, value):
        return self.collection.find({key : value}).count()

    def countAll(self):
        return self.collection.count()



