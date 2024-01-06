from .mongo import MongoDB
from bson import ObjectId
import datetime
from datetime import date, timedelta

class DisplayDate:
    def __init__(self, collection):
        self.db = MongoDB(collection)
        self.collection = collection

    def display_date(self):
        try:
            existingData = list(self.db.get({}))
        except Exception as e:
            print("Error retrieving data from database")

        if existingData:
            while True:
                try:
                    date = input("Enter date (MM/DD/YY): ")
                    parsed_date = datetime.datetime.strptime(date, "%m/%d/%y")
                    break
                except ValueError:
                    print("Incorrect data format, should be MM/DD/YY")
            if self.collection == "sleep":
                query = {
                    "time_end": {"$gte": parsed_date, "$lte": parsed_date + timedelta(days=1)},
                }
            else:
                query = {
                    "date": parsed_date
                }
            try:
                filteredData = list(self.db.get(query))
            except Exception as e:
                print(e)
                print("Error retrieving data from database\n")
            if filteredData:
                keys = list(filteredData[0].keys())
                for index, i in enumerate(filteredData):
                    j = index + 1 
                    output = f"Record {j}: \n"
                    for key in keys:
                        output += f"{key}: {i[key]}\n"
                    if j == len(filteredData):
                        print("")
                        print(output)
                        print("")
                    else:
                        print("")
                        print(output)
            else:
                print("No data to display for that date")
        else:
            print("No data to display")
            print("Exiting...\n")
