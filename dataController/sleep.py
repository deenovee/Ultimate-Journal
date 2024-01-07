from functions.mongo import MongoDB
from functions.delete import Delete
from functions.display import Display
from functions.filter import Filter
from functions.display_all import DisplayAll
from functions.display_date import DisplayDate
from functions.update import Update
from functions.inputs import Inputs
import pymongo
import datetime
from datetime import date, timedelta
from bson import ObjectId

class Sleep:
    def __init__(self):
        self.db = MongoDB("sleep")
        self.delete = Delete("sleep")
        self.display = Display("sleep")
        self.filter = Filter("sleep")
        self.display_all = DisplayAll("sleep")
        self.display_date = DisplayDate("sleep")
        self.update = Update("sleep")
        self.inputs = Inputs()

    def close(self):
        self.db.close()
    
    def displayData(self):
        try:
            self.display.display()
        except Exception as e:
            print(e)
            print("Error displaying data")

    def filterData(self):
        try:
            self.filter.filter()
        except Exception as e:
            print(e)
            print("Error filtering data")

    def displayAllData(self):
        try:
            self.display_all.display_all()
        except Exception as e:
            print(e)
            print("Error displaying all data")

    def displaySingleDate(self):
        try:
            self.display_date.display_date()
        except Exception as e:
            print(e)
            print("Error displaying single date")

    def deleteData(self):
        try:
            self.delete.delete()
        except Exception as e:
            print(e)
            print("Error deleting data")

    def updateData(self):
        try:
            self.update.update()
        except Exception as e:
            print(e)
            print("Error updating data")

    def collectData(self):
        try:
            print("Enter Start Date")
            parsed_start_date = self.inputs.get_date()
            print("Enter Start Time")
            parsed_start_time = self.inputs.get_time()
            
            start_timestamp =  datetime.datetime.combine(parsed_start_date, parsed_start_time.time())

            print("Enter End Date")
            parsed_end_date = self.inputs.get_date()
            print("Enter End Time")
            parsed_end_time = self.inputs.get_time()

            end_timestamp = datetime.datetime.combine(parsed_end_date, parsed_end_time.time())

            print("Enter sleep quality (1-10): ")
            while True:
                quality = self.inputs.get_int()
                if quality < 1 or quality > 10:
                    print("Quality must be between 1 and 10")
                else:
                    break

            while True:
                nap = input("Nap? (y/n): ")
                try: 
                    nap = nap.lower()
                    if nap == "y":
                        nap = True
                        break
                    elif nap == "n":
                        nap = False
                        break
                    else:
                        print("Enter y or n")
                except ValueError:
                    print("Invalid input")

            hours = self.update.calculate_hours(start_timestamp, end_timestamp)
            sleep_record = {
                "time_start": start_timestamp,
                "time_end": end_timestamp,
                "hours": hours,
                "quality": quality,
                "nap": nap
            }
            self.db.insert(sleep_record)
            print("Sleep record added successfully\n")

        except pymongo.errors.PyMongoError as e:
            print(f"Failed to insert record into MongoDB: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
        
        self.displayData()

