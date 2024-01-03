import pymongo
import datetime
from datetime import date, timedelta
from bson import ObjectId

class Sleep:
    def __init__(self):
        try:
            self.client = pymongo.MongoClient("mongodb://localhost:27017/")
            self.db = self.client["MyDashboard"]
            self.collection = self.db["sleep"]
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
    
    def displayData(self):
        start_date = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=8)  # Adjust the number of days as needed

        # Define the query to filter records within the date range
        query = {
            "time_end": {
                "$gte": start_date
            }
        }
        try:
            sleep_records = list(self.get(query))
        except pymongo.errors.PyMongoError as e:
            print(f"Failed to retrieve data from MongoDB: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

        if sleep_records == []:
            print("No sleep data for the past week")
        else:
            print("Sleep Weekly Overview: \n")

            # display sleep data 
            for index, i in enumerate(sleep_records):
                j = index + 1
                if j == len(sleep_records):
                    print("")
                    print(f"Record {j}:\n ObjectId: {i['_id']}\n Start: {i['time_start'].strftime('%Y-%m-%d %H:%M:%S')}\n End: {i['time_end'].strftime('%Y-%m-%d %H:%M:%S')}\n Hours: {i['hours']}\n Quality: {i['quality']}\n Nap: {i['nap']}")
                    print("")
                else:
                    print("")
                    print(f"Record {j}:\n ObjectId: {i['_id']}\n Start: {i['time_start'].strftime('%Y-%m-%d %H:%M:%S')}\n End: {i['time_end'].strftime('%Y-%m-%d %H:%M:%S')}\n Hours: {i['hours']}\n Quality: {i['quality']}\n Nap: {i['nap']}")

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
            self.insert(sleep_record)
            print("Sleep record added successfully\n")

        except pymongo.errors.PyMongoError as e:
            print(f"Failed to insert record into MongoDB: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
        
        self.displayData()

    def deleteData(self):
        try:
            existingData = list(self.get({}))
        except Exception as e:
            print("Error retrieving data from database")
        if existingData:
            try:
                while True:
                    id = input("Enter Object ID to delete or list of IDs separated by /: ")
                    try:
                        id = str(id)
                        break
                    except ValueError:
                        print(ValueError)
                query = {"_id": id}
                try:
                    self.delete(query)
                    print("Exercise data deleted successfully")
                except pymongo.errors.PyMongoError as e:
                    print(f"Failed to delete document: {e}")
                except Exception as e:
                    print(f"An error occurred: {e}")
            except KeyboardInterrupt:
                print("")
                print("Exiting...")
                print("")
            self.displayData()
        else:
            print("No data to delete")
            print("Exiting...\n")


    def updateData(self):
        try:
            existingData = list(self.get({}))
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
            objectToUpdate = self.get_by_id(idToUpdate)
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
                        query = {"_id": ObjectId(objectId)}
                        update_query = {"$set": {f"{selectedKey}": newValue}}
                        break
                    else:
                        print("Invalid input, try again.")
                
            try:
                self.update(query, update_query)
                if userInput == 2:
                    hours = self.calculateHours(combined_datetime, objectToUpdate["time_end"])
                    self.update(query, {"$set": {"hours": hours}})

                elif userInput == 3:
                    hours = self.calculateHours(objectToUpdate["time_start"], combined_datetime)
                    self.update(query, {"$set": {"hours": hours}})

            except Exception as e:
                print(e)
                print("Error updating data in database")

            self.displayData()
        else:
            print("No data to update")
            print("Exiting...")

    def filterData(self):
        try:
            existingData = list(self.get({}))
        except Exception as e:
            print("Error retrieving data from database")

        if existingData:
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

            query = {
                "time_start": {
                    "$gte": parsed_start_date,
                    "$lte": parsed_end_date
                }
            }
            try:
                filteredData = list(self.get(query))
            except Exception as e:
                print("Error retrieving data from database")
            if filteredData:
                print("\nFiltered Sleep Data: \n")
                for index, i in enumerate(filteredData):
                    j = index + 1
                    if j == len(filteredData):
                        print("")
                        print(f"Record {j}:\n ObjectId: {i['_id']}\n Start: {i['time_start'].strftime('%Y-%m-%d %H:%M:%S')}\n End: {i['time_end'].strftime('%Y-%m-%d %H:%M:%S')}\n Hours: {i['hours']}\n Quality: {i['quality']}\n Nap: {i['nap']}")
                        print("")
                    else:
                        print("")
                        print(f"Record {j}:\n ObjectId: {i['_id']}\n Start: {i['time_start'].strftime('%Y-%m-%d %H:%M:%S')}\n End: {i['time_end'].strftime('%Y-%m-%d %H:%M:%S')}\n Hours: {i['hours']}\n Quality: {i['quality']}\n Nap: {i['nap']}")
            else:
                print("No data found for that date range")
        else:
            print("No data to filter")
            print("Exiting...")

    def displayAllData(self):
        try:
            existingData = list(self.get({}))
        except Exception as e:
            print("Error retrieving data from database")
        if existingData:
            for index, i in enumerate(existingData):
                j = index + 1
                if j == len(existingData):
                    print("")
                    print(f"Record {j}:\n ObjectId: {i['_id']}\n Start: {i['time_start'].strftime('%Y-%m-%d %H:%M:%S')}\n End: {i['time_end'].strftime('%Y-%m-%d %H:%M:%S')}\n Hours: {i['hours']}\n Quality: {i['quality']}\n Nap: {i['nap']}")
                    print("")
                else:
                    print("")
                    print(f"Record {j}:\n ObjectId: {i['_id']}\n Start: {i['time_start'].strftime('%Y-%m-%d %H:%M:%S')}\n End: {i['time_end'].strftime('%Y-%m-%d %H:%M:%S')}\n Hours: {i['hours']}\n Quality: {i['quality']}\n Nap: {i['nap']}")

        else:
            print("No data to display")
            print("Exiting...")

    def displaySingleDate(self):
        try:
            existingData = list(self.get({}))
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
            query = {
                "time_end": {
                    "$gte": parsed_date,
                    "$lt": parsed_date + timedelta(days=1)
                }
            }
            try:
                filteredData = list(self.get(query))
            except Exception as e:
                print(e)
                print("Error retrieving data from database\n")
            if filteredData:
                for index, i in enumerate(filteredData):
                    j = index + 1 
                    if j == len(filteredData):
                        print("")
                        print(f"Record {j}:\n ObjectId: {i['_id']}\n Start: {i['time_start'].strftime('%Y-%m-%d %H:%M:%S')}\n End: {i['time_end'].strftime('%Y-%m-%d %H:%M:%S')}\n Hours: {i['hours']}\n Quality: {i['quality']}\n Nap: {i['nap']}")
                        print("")
                    else:
                        print("")
                        print(f"Record {j}:\n ObjectId: {i['_id']}\n Start: {i['time_start'].strftime('%Y-%m-%d %H:%M:%S')}\n End: {i['time_end'].strftime('%Y-%m-%d %H:%M:%S')}\n Hours: {i['hours']}\n Quality: {i['quality']}\n Nap: {i['nap']}")
            else:
                print("No data to display")