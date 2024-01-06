from functions.mongo import MongoDB
from functions.delete import Delete
from functions.display import Display
from functions.filter import Filter
from functions.display_all import DisplayAll
from functions.display_date import DisplayDate
import datetime
from datetime import date, timedelta
from bson import ObjectId

class TimeKeeper:
    def __init__(self):
        self.db = MongoDB("timeKeeper")
        self.delete = Delete("timeKeeper")
        self.display = Display("timeKeeper")
        self.filter = Filter("timeKeeper")
        self.display_all = DisplayAll("timeKeeper")
        self.display_date = DisplayDate("timeKeeper")

    def close(self):
        self.db.close()

    #function to display data
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
            print("Error deleting data from database")

    def collectData(self):
        try:
            while True:
                inputNumber = input("Enter number of inputs: ")
                try:
                    inputNumber = int(inputNumber)
                    if 1 <= inputNumber <= 10:
                        break
                    else:
                        print("Invalid input. Please enter a number between 1 and 10.")
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
            
            while True:
                date = input("Enter date (MM/DD/YY): ")
                try:
                    date = datetime.datetime.strptime(date, "%m/%d/%y").replace(hour=0, minute=0, second=0, microsecond=0)
                    break
                except ValueError:
                    print(ValueError)

            for i in range(int(inputNumber)):
                while True:
                    inputTime = input("Enter time in minutes: ")
                    try:
                        inputTime = int(inputTime)
                        break
                    except ValueError:
                        print("Invalid input")
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
                data = {
                    "date": date,
                    "time": inputTime,
                    "description": inputDescription,
                    "category": categoryChoice
                }
                try:
                    self.db.insert(data)
                except Exception as e:
                    print(e)
                    print("Error inserting data into database")

        except KeyboardInterrupt:
            print("Exiting...")
        except Exception as e:
            print(e)
            print("Error handling data input")
            
        self.displayData()
    
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
                self.db.update(query, update_query)
            except Exception as e:
                print(e)
                print("Error updating data in database")

            self.displayData()
        else:
            print("No data to update")
            print("Exiting...")
