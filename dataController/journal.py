import datetime
import pymongo
from pymongo import MongoClient
from bson import ObjectId

class Journal:
    def __init__(self):
        try:
            self.client = pymongo.MongoClient("mongodb://localhost:27017/")
            self.db = self.client["MyDashboard"]
            self.collection = self.db["journal"]
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

    def get_one(self):
        return self.collection.find_one(sort=[("date", 1)])

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

    def displayRecentJournal(self):
        #display last entry
        try:
            latest_entry = self.get_one()
            if latest_entry:
                print(f"Record:\n _id = {latest_entry['_id']}\ndate = {latest_entry['date']}\nJOURNAL\n{latest_entry['journal']}")
            else:
                print("No data to display")
        except Exception as e:
            print(e)
            print("Error retrieving data from database")
    
    def collectData(self):
        while True:
            date = input("Enter date (MM/DD/YY): ")
            try:
                date = datetime.datetime.strptime(date, "%m/%d/%y").replace(hour=0, minute=0, second=0, microsecond=0)
                break
            except ValueError:
                print(ValueError)
        #validate minutes input
        print("Start journal below:")
        inputText = ""  # Initialize inputText outside the loop
        while True:
            entry = input("Enter your journal text (press Enter to finish):\n")
            if entry:
                inputText += entry + "\n"
                break
        while True:
            finished = input("Finished? (y/n): ")
            try:
                if finished.lower() == "y":
                    break
                elif finished.lower() == "n":
                    print(inputText)
                    while True:
                        entry = input("Restart or Add on?(1/2):\n")
                        try:
                            entry = int(entry)
                            if entry == 1:
                                inputText = input("Enter new text below:\n") + "\n"
                                break
                            elif entry == 2:
                                newInputText = input("Enter new text below:\n")
                                inputText += newInputText + "\n"
                                break
                            else:
                                print("Invalid input")
                        except Exception as e:
                            print(e)
                            print("Error handling restart/add on input")
                        
            except Exception as e:
                print(e)
                print("Error handling finished input")

        while True:
            inputRating = input("Rate day based on efficiency (1-10): ")
            try:
                inputRating = int(inputRating)
                if inputRating > 10 or inputRating < 1:
                    print("must be between 1 and 10")
                else:
                    break
            except Exception as e:
                print(e)
                print("Error handling rating input")
        
        #create a dictionary to store data
        dataDict = {
            "date": date,
            "journal": inputText,
            "rating": inputRating
        }
        #insert data into database
        try:
            self.insert(dataDict)
        except Exception as e:
            print(e)
            print("Error inserting data into database")
        
        self.displayRecentJournal()

    def deleteData(self):
        #get data from user
        try:
            existingData = list(self.get({}))
        except Exception as e:
            print("Error retrieving data from database")
        if existingData:
            while True:
                objectId = str(input("Enter Object ID to delete or list of IDs separated by /: "))
                if objectId:
                    break
            #get data from database
            objectToDelete = {"_id": objectId}
            #delete data from database
            try:
                self.delete(objectToDelete)
            except Exception as e:
                print(e)
                print("Error deleting data from database")

            self.displayRecentJournal()
        else:
            print("No data to delete")
            print("Exiting...")

    def updateData(self):
        try:
            existingData = list(self.get({}))
        except Exception as e:
            print("Error retrieving data from database")

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

            while True:
                newValue = input("Enter new value: ")
                if newValue:
                    query = {"_id": ObjectId(id)}
                    update_query = {"$set": {f"{selectedKey}": newValue}}
                    break
                else:
                    print("Invalid input try again.")
            
            try:
                self.update(query, update_query)
            except Exception as e:
                print(e)
                print("Error updating data in database")

            self.displayRecentJournal()
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
                "date": {
                    "$gte": parsed_start_date,
                    "$lte": parsed_end_date
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
                        print(f"Record {j}:\n _id = {i['_id']}\ndate = {i['date']}\nJOURNAL\n{i['journal']}")
                        print("")
                    else:
                        print("")
                        print(f"Record {j}:\n _id = {i['_id']}\ndate = {i['date']}\nJOURNAL\n{i['journal']}")
            else:
                print("No data to display")
        else:
            print("No data to filter")
            print("Exiting...")

    def displayAllData(self):
        try:
            existingData = list(self.get({}))
        except Exception as e:
            print("Error retrieving data from database")
        if existingData:
            # if there are more than 25 data objects, display only the first 25
            for index, i in enumerate(existingData):
                j = index + 1
                if j == len(existingData):
                    print("")
                    print(f"Record {j}:\n _id = {i['_id']}\ndate = {i['date']}\nJOURNAL\n{i['journal']}")
                    print("")
                else:
                    print("")
                    print(f"Record {j}:\n _id = {i['_id']}\ndate = {i['date']}\nJOURNAL\n{i['journal']}")
