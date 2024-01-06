from .mongo import MongoDB
from bson import ObjectId
import datetime
from datetime import date, timedelta

class Display:
    def __init__(self, collection):
        self.db = MongoDB(collection)
        self.collection = collection

    def display(self):
        if self.collection == "journal":
            start_date = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
            query = {"date": {"$gte": start_date}}
        elif self.collection == "sleep":
            print("Displaying sleep data for the past week")
            start_date = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=7)
            query = {"time_end": {"$gte": start_date}}
        else:
            start_date = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=7)
            query = {"date": {"$gte": start_date}}

        try:
            records = list(self.db.get(query))
        except Exception as e:
            print("Error retrieving data from database")
            print(e)

        if records == []:
            print("No data to display")
        else:
            keys = records[0].keys()
            for index, i in enumerate(records):
                j = index + 1
                output = f"Record {j}: \n"
                for key in keys:
                    output += f"{key}: {i[key]}\n"
                if j == len(records):
                    print("")
                    print(output)
                    print("")
                else:
                    print("")
                    print(output)
                    