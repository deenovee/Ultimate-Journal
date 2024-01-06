from functions.mongo import MongoDB
from functions.delete import Delete
from functions.display import Display
from functions.filter import Filter
from functions.display_all import DisplayAll
from functions.display_date import DisplayDate
import datetime
from datetime import timedelta
import pymongo
from bson import ObjectId

class Journal:
    def __init__(self):
        self.db = MongoDB("journal")
        self.delete = Delete("journal")
        self.display = Display("journal")
        self.filter = Filter("journal")
        self.display_all = DisplayAll("journal")
        self.display_date = DisplayDate("journal")

    def close(self):
        self.db.close()

    def displayRecentJournal(self):
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
