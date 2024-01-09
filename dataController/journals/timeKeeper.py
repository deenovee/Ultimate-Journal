from dataController.functions.mongo import MongoDB
from dataController.functions.delete import Delete
from dataController.functions.display import Display
from dataController.functions.filter import Filter
from dataController.functions.display_all import DisplayAll
from dataController.functions.display_date import DisplayDate
from dataController.functions.update import Update
from dataController.functions.inputs import Inputs
import datetime
from datetime import date, timedelta
from bson import ObjectId

class TimeKeeper:
    __name__ = "TimeKeeper"
    
    def __init__(self):
        self.db = MongoDB("timeKeeper")
        self.delete = Delete("timeKeeper")
        self.display = Display("timeKeeper")
        self.filter = Filter("timeKeeper")
        self.display_all = DisplayAll("timeKeeper")
        self.display_date = DisplayDate("timeKeeper")
        self.update = Update("timeKeeper")
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
            print("Error deleting data from database")

    def updateData(self):
        try:
            self.update.update()
        except Exception as e:
            print(e)
            print("Error updating data")

    def collectData(self):
        try:
            print("Enter number of inputs: ")
            inputNumber = self.inputs.get_int()
            print("Enter date below:")
            date = self.inputs.get_date()

            for i in range(int(inputNumber)):
                print("Enter time in minutes: ")
                inputTime = self.inputs.get_int()

                while True:
                    inputDescription = input("Enter description: ")
                    try:
                        if inputDescription:
                            break
                        else:
                            print("Invalid input")
                    except ValueError:
                        print("Please add a description")
                
                categoryList = ['HEALTH', 'WORK', 'PROJECT', 'EDUCATION', 'READING', 'HOBBY', 'NETWORKING', 'OTHER']
                categoryChoice = self.inputs.get_list_choice(categoryList)
                
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
