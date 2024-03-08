from dataController.functions.mongo import MongoDB
from bson import ObjectId
import datetime
from datetime import date, timedelta

class Filter:
    def __init__(self, collection):
        self.db = MongoDB(collection)
        self.collection = collection

    def filter(self):
        try:
            existingData = list(self.db.get({}))
        except Exception as e:
            print("Error retrieving data from database")
        if existingData and self.collection != "assets":
            while True:
                try:
                    date_start = input("Enter start date (MM/DD/YY): ")
                    parsed_start_date = datetime.datetime.strptime(date_start, "%m/%d/%y")
                    break
                except ValueError:
                    print("Incorrect data format, should be MM/DD/YY")
            while True:
                try:
                    date_end = input("Enter end date (MM/DD/YY): ")
                    parsed_end_date = datetime.datetime.strptime(date_end, "%m/%d/%y")
                    break
                except ValueError:
                    print("Incorrect data format, should be MM/DD/YY")

            if self.collection =="sleep":
                query = {
                    "time_end": {
                        "$gte": parsed_start_date,
                        "$lte": parsed_end_date
                    }
                }
            else:
                query = {
                    "date": {
                        "$gte": parsed_start_date,
                        "$lte": parsed_end_date
                    }
                }
                
            try:
                filteredData = list(self.db.get(query))
            except Exception as e:
                print(e)
                print("Error retrieving data from database\n")

            if filteredData:
                keys = filteredData[0].keys()
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
                print("No data to display for that range")
        elif self.collection == "assets":
            while True:
                try:
                    asset_type = input("Enter asset type: ")
                    break
                except ValueError:
                    print("Invalid input")

            query = {
                "type": asset_type
            }
            try:
                filteredData = list(self.db.get(query))
            except Exception as e:
                print(e)
                print("Error retrieving data from database\n")

            if filteredData:
                keys = filteredData[0].keys()
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
                print("No data to display")

        else:
            print("No data to display")

