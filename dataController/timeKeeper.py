import pymongo
import datetime
from datetime import date, timedelta
from bson import ObjectId

class TimeKeeper:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["MyDashboard"]
        self.collection = self.db["timeKeeper"]

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

    #function to display data
    def displayData(self):
        start_date = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(5)
        
        query = {
            "date": {
                    "$gte": start_date
            }
        }
        try:
            timekeeper_records = list(self.get(query))
        except pymongo.errors.PyMongoError as e:
            print(f"MongoDB query failed: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        # check if there are 25 or fewer data objects
        if len(timekeeper_records) == []:
            print("No timekeeper data to display")
        else:
            for index, i in enumerate(timekeeper_records):
                j = index + 1
                if j == len(timekeeper_records):
                    print("")
                    print(f"Record {index + 1}:\n _id = {i['_id']}\n date = {i['date']}\n time = {i['time']}\n description = {i['description']}\n category = {i['category']}\n")
                    print("")
                else:
                    print("")
                    print(f"Record {index + 1}:\n _id = {i['_id']}\n date = {i['date']}\n time = {i['time']}\n description = {i['description']}\n category = {i['category']}\n")

    #function to collect data from user
    def collectData(self):
        try:
            #get data from user
            while True:
                inputNumber = input("Enter number of inputs: ")

                try:
                    # Attempt to convert the input to an integer
                    inputNumber = int(inputNumber)

                    # Check if the entered number is a digit and within the range 1-10
                    if 1 <= inputNumber <= 10:
                        break
                    else:
                        print("Invalid input. Please enter a number between 1 and 10.")
                except ValueError:
                    print("Invalid input. Please enter a valid number.")

            #loop through the number of inputs
            for i in range(int(inputNumber)):
                while True:
                    date = input("Enter date (MM/DD/YY): ")
                    try:
                        date = datetime.datetime.strptime(date, "%m/%d/%y").replace(hour=0, minute=0, second=0, microsecond=0)
                        break
                    except ValueError:
                        print(ValueError)

                #validate minutes input
                while True:
                    inputTime = input("Enter time in minutes: ")
                    try:
                        inputTime = int(inputTime)
                        break
                    except ValueError:
                        print("Invalid input")
            #validate description input
                while True:
                    inputDescription = input("Enter description: ")
                    try:
                        if inputDescription:
                            break
                        else:
                            print("Invalid input")
                    except ValueError:
                        print("Please add a description")
                while True:
                    categoryList = ['HEALTH', 'WORK', 'PROJECT', 'EDUCATION', 'READING', 'HOBBY', 'NETWORKING', 'OTHER']
                    for index, i in enumerate(categoryList):
                        j = index + 1
                        print(f"{j} - {i}")
                    inputCategory = input("Enter category: ")
                    try:
                        inputCategory = int(inputCategory)
                        if 1 <= inputCategory <= len(categoryList):
                            categoryChoice = categoryList[inputCategory-1]
                            break
                        else:
                            print("Invalid input")
                    except ValueError:
                        print("Please add a category")
                #create a dictionary to store data
                data = {
                    "date": date,
                    "time": inputTime,
                    "description": inputDescription,
                    "category": categoryChoice
                }
                #insert data into database
                try:
                    self.insert(data)
                except Exception as e:
                    print(e)
                    print("Error inserting data into database")

        except KeyboardInterrupt:
            print("Exiting...")
        except Exception as e:
            print(e)
            print("Error handling data input")
            
        self.displayData()

    #function to delete data
    def deleteData(self):
        #get data from user
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

            if userInput == 2:
                while True:
                    date = input("Enter new date (MM/DD/YY): ")
                    try:
                        date = datetime.datetime.strptime(date, "%m/%d/%y").replace(hour=0, minute=0, second=0, microsecond=0)
                        query = {"_id": ObjectId(id)}
                        update_query = {"$set": {f"{selectedKey}": date}}
                        break
                    except ValueError:
                        print(ValueError)

            elif userInput == 3:   
                while True:
                    time = input("Enter new time in minutes: ")
                    try:
                        time = int(time)
                        query = {"_id": ObjectId(id)}
                        update_query = {"$set": {f"{selectedKey}": time}}
                        break
                    except ValueError:
                        print(ValueError)

            elif userInput == 5:
                categoryList = ['HEALTH', 'WORK', 'PROJECT', 'EDUCATION', 'READING', 'HOBBY', 'NETWORKING', 'OTHER']
                for index, i in enumerate(categoryList):
                    j = index + 1
                    print(f"{j} - {i}")
                while True:
                    category = input("Enter new category: ")
                    try:
                        category = int(category)
                        if 1 <= category <= len(categoryList):
                            categoryChoice = categoryList[category-1]
                            query = {"_id": ObjectId(id)}
                            update_query = {"$set": {f"{selectedKey}": categoryChoice}}
                            break
                    except ValueError:
                        print(ValueError)

            else:  
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

            self.displayData()
        else:
            print("No data to update")
            print("Exiting...")

    #function to filter data for a single date
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
                        print(f"Record {index + 1}:\n _id = {i['_id']}\n date = {i['date']}\n time = {i['time']}\n description = {i['description']}\n category = {i['category']}\n")
                        print("")
                    else:
                        print("")
                        print(f"Record {index + 1}:\n _id = {i['_id']}\n date = {i['date']}\n time = {i['time']}\n description = {i['description']}\n category = {i['category']}\n")
            else:
                print("No data for that date range")
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
                    print(f"Record {index + 1}:\n _id = {i['_id']}\n date = {i['date']}\n time = {i['time']}\n description = {i['description']}\n category = {i['category']}\n")
                    print("")
                else:
                    print("")
                    print(f"Record {index + 1}:\n _id = {i['_id']}\n date = {i['date']}\n time = {i['time']}\n description = {i['description']}\n category = {i['category']}\n")
        else:
            print("No data to display")
            print("Exiting...\n")