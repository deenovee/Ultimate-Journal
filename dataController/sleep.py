from functions.mongo import MongoDB
from functions.delete import Delete
from functions.display import Display
from functions.filter import Filter
from functions.display_all import DisplayAll
from functions.display_date import DisplayDate
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

    def calculateHours(self, date_time1, date_time2):
        try:
            if not isinstance(date_time1, datetime.datetime) or not isinstance(date_time2, datetime.datetime):
                raise ValueError("Input times must be datetime.datetime objects")

            difference = date_time2 - date_time1

            hours = difference.total_seconds() / 3600
            return hours
        except ValueError:
            print("Incorrect data format, should be HH:MM")
        except Exception as e:
            print(f"An error occurred: {e}")

    def collectData(self):
        try:

            while True:
                date_start = input("Enter start date (MM/DD/YY): ")
                try:
                    parsed_start_date = datetime.datetime.strptime(date_start, "%m/%d/%y")
                    break
                except ValueError:
                    print("Incorrect data format, should be MM/DD/YY")
            while True:
                time_start = input("Enter start time (HH:MM): ")
                try:
                    parsed_start_time = datetime.datetime.strptime(time_start, "%H:%M")
                    break
                except ValueError:
                    print("Incorrect data format, should be HH:MM")
            
            start_timestamp =  datetime.datetime.combine(parsed_start_date, parsed_start_time.time())

            while True:
                date_end = input("Enter end date (MM/DD/YY): ")
                try:
                    parsed_end_date = datetime.datetime.strptime(date_end, "%m/%d/%y")
                    break
                except ValueError:
                    print("Incorrect data format, should be MM/DD/YY")
            while True:
                time_end = input("Enter end time (HH:MM): ")
                try:
                    parsed_end_time = datetime.datetime.strptime(time_end, "%H:%M")
                    break
                except ValueError:
                    print("Incorrect data format, should be HH:MM")

            end_timestamp = datetime.datetime.combine(parsed_end_date, parsed_end_time.time())

            while True:
                quality = input("Enter sleep quality (1-10): ")
                try:
                    quality = int(quality)
                    if quality < 1 or quality > 10:
                        print("Quality must be between 1 and 10")
                    else:
                        break
                except ValueError:
                    print("Quality must be an integer")

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

            hours = self.calculateHours(start_timestamp, end_timestamp)
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

    def updateData(self):
        try:
            existingData = list(self.db.get({}))
        except Exception as e:
            print("\nError retrieving data from database\n")

        if existingData:
            while True:
                id = input("Enter Object ID to update: ")
                try:
                    id = str(id)
                    break
                except ValueError:
                    print(ValueError)

            idToUpdate = {"_id": id}
            objectToUpdate = self.db.get_by_id(idToUpdate)
            keys = list(objectToUpdate.keys())
            for i in range(len(keys)):
                print(f"{i+1} - {keys[i]}")

            while True:
                try:
                    userInput = input("Select the key to update: ")
                    userInput = int(userInput)
                    if 1 < userInput <= len(keys):
                        selectedKey = keys[userInput-1]
                        break
                    elif userInput == 1:
                        print("Cannot update Object ID")
                    else:
                        print("Invalid input.")
                except ValueError:
                    print("Invalid input try again.")

            if userInput == 2 or userInput == 3:
                while True:
                    new_time= input("Enter new value (HH:MM): ")
                    try:
                        new_time = datetime.datetime.strptime(new_time, "%H:%M").time()
                        break
                    except ValueError:
                        print("Incorrect data format, should be HH:MM")
                while True:
                    new_date = input("Enter new date (MM/DD/YY): ")
                    try:
                        new_date = datetime.datetime.strptime(new_date, "%m/%d/%y").date()
                        break
                    except ValueError:
                        print("Incorrect data format, should be MM/DD/YY")
                combined_datetime = datetime.datetime.combine(new_date, new_time)
                try:
                    query = {"_id": ObjectId(id)}
                    update_query = {"$set": {f"{selectedKey}": combined_datetime}}
                except pymongo.errors.PyMongoError as e:
                    print(f"Error: {e}\nError updating data in database")
                except Exception as e:
                    print("An unexpected error occurred: {e}")
            else:
                while True:
                    newValue = input("Enter new value: ")
                    if newValue:
                        query = {"_id": ObjectId(id)}
                        update_query = {"$set": {f"{selectedKey}": newValue}}
                        break
                    else:
                        print("Invalid input, try again.")
                
            try:
                self.db.update(query, update_query)
                if userInput == 2:
                    hours = self.calculateHours(combined_datetime, objectToUpdate["time_end"])
                    self.db.update(query, {"$set": {"hours": hours}})

                elif userInput == 3:
                    hours = self.calculateHours(objectToUpdate["time_start"], combined_datetime)
                    self.db.update(query, {"$set": {"hours": hours}})

            except Exception as e:
                print(e)
                print("Error updating data in database")

            self.displayData()
        else:
            print("No data to update")
            print("Exiting...")
