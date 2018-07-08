import pymongo
from pymongo import MongoClient

class User(object):

    def get_first_name(self, email):
        client = MongoClient('localhost', 27017)
        db = client['greetydb']
        collection = db['users']
        result = collection.find_one({"email" : email}, {"_id" : 0, "firstname" : 1})
        return result['firstname']

    def check_duplicate_user(self, email):
        client = MongoClient('localhost', 27017)
        db = client['greetydb']
        collection = db['users']
        result = collection.find({"email" : email},{"_id" : 0, "firstname" : 1}).count()
        if result == 0:
            return False
        else:
            return True        







