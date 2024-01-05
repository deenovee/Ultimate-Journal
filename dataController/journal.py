from mongo import MongoDB
import datetime
from datetime import timedelta
import pymongo
from bson import ObjectId

class Journal:
    def __init__(self):
        self.db = MongoDB("journal")

    def close(self):
        self.db.close()

    def displayRecentJournal(self):
        date = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
        query = {"date": date}
        try:
            latest_entry = list(self.db.get(query))
            if latest_entry:
                for entry in latest_entry:
                    print("")
                    print(f"Record:\n _id = {entry['_id']}\ndate = {entry['date']}\nJOURNAL\n{entry['journal']}")
                    print("")
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
            self.db.insert(dataDict)
        except Exception as e:
            print(e)
            print("Error inserting data into database")
        
        self.displayRecentJournal()

    def deleteData(self):
        #get data from user
        try:
            existingData = list(self.db.get({}))
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
                self.db.delete(objectToDelete)
            except Exception as e:
                print(e)
                print("Error deleting data from database")

            self.displayRecentJournal()
        else:
            print("No data to delete")
            print("Exiting...")

    def updateData(self):
        try:
            existingData = list(self.db.get({}))
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
            if userInput == 2:
                while True:
                    newValue = input("Enter new value (MM/DD/YY): ")
                    try:
                        newValue = datetime.datetime.strptime(newValue, "%m/%d/%y").replace(hour=0, minute=0, second=0, microsecond=0)
                        query = {"_id": ObjectId(id)}
                        update_query = {"$set": {f"{selectedKey}": newValue}}
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
                self.db.update(query, update_query)
            except Exception as e:
                print(e)
                print("Error updating data in database")

            self.displayRecentJournal()
        else:
            print("No data to update")
            print("Exiting...")

    def filterData(self):
        try:
            existingData = list(self.db.get({}))
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
                filteredData = list(self.db.get(query))
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
            existingData = list(self.db.get({}))
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

    def displaySingleDate(self):
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
            query = {
                "date": parsed_date
            }
            try:
                filteredData = list(self.db.get(query))
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
