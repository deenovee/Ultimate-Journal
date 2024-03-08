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

class Liabilities:
    __name__ = "Liabilities"
    
    def __init__(self):
        self.db = MongoDB("liabilities")
        self.delete = Delete("liabilities")
        self.display_all = DisplayAll("liabilities")
        self.filter = Filter("liabilities")
        self.update = Update("liabilities")
        self.inputs = Inputs()

    def close(self):
        self.db.close()
    
    def filterData(self):
        try:
            self.filter.filter()
        except Exception as e:
            print(e)
            print("Error filtering data")

    def deleteData(self):
        try:
            self.delete.delete()
        except Exception as e:
            print(e)
            print("Error deleting data")

    def displayAllData(self):
        try:
            self.display_all.display_all()
        except Exception as e:
            print(e)
            print("Error displaying all data")

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

            for i in range(int(inputNumber)): 
                print(f"Enter liability {i+1} name:")
                name = self.inputs.get_string()
                print("What is the amount of the liability? ")
                amount = self.inputs.get_float()
                print(f"Liabilility {i+1} description: ")
                description = self.inputs.get_string()
                
                data = {
                    "liability_name": name,
                    "liability_amount": amount,
                    "liability_description": description
                }

                try:
                    self.db.insert(data)
                except Exception as e:
                    print(e)
                    print("Error inserting data")
        except Exception as e:
            print(e)
            print("Error collecting data")
        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            print("Exiting...")
            print("")
        
        self.display_all.display_all()
                
        