from dataController.functions.mongo import MongoDB
from dataController.functions.delete import Delete
from dataController.functions.display import Display
from dataController.functions.filter import Filter
from dataController.functions.display_all import DisplayAll
from dataController.functions.display_date import DisplayDate
from dataController.functions.update import Update
from dataController.functions.inputs import Inputs
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
        self.update = Update("journal")
        self.inputs = Inputs()

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

    def updateData(self):
        try:
            self.update.update()
        except Exception as e:
            print(e)
            print("Error updating data")
    
    def collectData(self):
        print("Enter date below:")
        date = self.inputs.get_date()
        print("Start journal below:")
        inputText = ""  
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

        print("Rate day based on efficiency (1-10): ")
        while True:
            inputRating = self.inputs.get_int()
            if inputRating < 1 or inputRating > 10:
                print("Rating must be between 1 and 10")
            else:
                break        

        dataDict = {
            "date": date,
            "journal": inputText,
            "rating": inputRating
        }

        try:
            self.db.insert(dataDict)
        except Exception as e:
            print(e)
            print("Error inserting data into database")
        
        self.displayRecentJournal()


