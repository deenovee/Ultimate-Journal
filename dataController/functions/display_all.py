from dataController.functions.mongo import MongoDB
from bson import ObjectId
import datetime
from datetime import date, timedelta

class DisplayAll:
    def __init__(self, collection):
        self.db = MongoDB(collection)
        self.collection = collection
    
    def display_all(self):
        try:
            existingData = list(self.db.get({}))
        except Exception as e:
            print("Error retrieving data from database")

        if existingData:
            keys = existingData[0].keys()
            for index, i in enumerate(existingData):
                j = index + 1
                output = f"Record {j}: \n"
                for key in keys:
                    output += f"{key}: {i[key]}\n"
                if j == len(existingData):
                    print("")
                    print(output)
                    print("")
                else:
                    print("")
                    print(output)
        else:
            print("No data to display")
            print("Exiting...\n")