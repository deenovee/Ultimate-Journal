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

class Assets:
    __name__ = "Assets"
    
    def __init__(self):
        self.db = MongoDB("assets")
        self.delete = Delete("assets")
        self.display_all = DisplayAll("assets")
        self.filter = Filter("assets")
        self.update = Update("assets")
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
            print("When did you acquire this asset? ")
            date = self.inputs.get_date()

            for i in range(int(inputNumber)):
                print(f"Enter asset {i+1} name: ")
                name = self.inputs.get_string()
                print(f"Enter asset {i+1} value: ")
                value = self.inputs.get_float()
                print(f"Enter asset {i+1} type: ")
                category_list = ["metal", "crypto", "stock", "real estate", "other"]
                asset_type = self.inputs.get_string()
                print(f"Enter asset {i+1} description: ")
                description = self.inputs.get_string()

                data = {
                    "purchase_date": date,
                    "asset_name": name,
                    "asset_value": value,
                    "asset_type": asset_type,
                    "asset_description": description
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
            self.close()
            exit()

        self.display_all.display_all()











