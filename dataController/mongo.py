import pymongo
import datetime
from datetime import date, timedelta
from bson import ObjectId

class MongoDB:
    def __init__(self, collection):
        try:
            self.client = pymongo.MongoClient("mongodb://localhost:27017/")
            self.db = self.client["MyDashboard"]
            self.collection = self.db[collection]
        except pymongo.errors.ConnectionFailure as e:
            print(f"Failed to connect to MongoDB: {e}")

    def insert(self, data):
        try:
            self.collection.insert_one(data)
        except pymongo.errors.PyMongoError as e:
            print(f"Failed to insert document: {e}")

    def get(self, query):
        try:
            return self.collection.find(query)
        except pymongo.errors.PyMongoError as e:
            print(f"MongoDB query failed: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def get_by_id(self, id):
        try:
            return self.collection.find_one({"_id": ObjectId(id['_id'])})
        except pymongo.errors.PyMongoError as e:
            print(f"MongoDB query failed: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def delete(self, data):
        if "/" in data["_id"]:
            try:
                objectIds = data["_id"].split("/")
                for i in objectIds:
                    query = {"_id": ObjectId(i)}
                    self.collection.delete_one(query)
                    print("Record deleted")
            except Exception as e:
                print(e)
                print("Error handling multpiple ids")
                print("trying single id")
        else:
            query = {"_id": ObjectId(data["_id"])}
            try:
                self.collection.delete_one(query)
                print("Record deleted")
            except Exception as e:
                print(e)
                print("Error deleting data from database")
    
    def update(self, query, update_query):
        try:
            print("Updating...")
            self.collection.update_one(query, update_query)
            print("Record updated")
        except Exception as e:
            print(e)
            print("Error updating data in database")

    def close(self):
        self.client.close()