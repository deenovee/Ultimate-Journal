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

class Nutrition:
    __name__ = "Nutrition"

    def __init__(self):
        self.db = MongoDB("nutrition")
        self.delete = Delete("nutrition")
        self.display = Display("nutrition")
        self.filter = Filter("nutrition")
        self.display_all = DisplayAll("nutrition")
        self.display_date = DisplayDate("nutrition")
        self.update = Update("nutrition")
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
            print("Error deleting data")

    def updateData(self):
        try:
            self.update.update()
        except Exception as e:
            print(e)
            print("Error updating data")

    def collectData(self):
        try:
            print("Enter number of inputs: ")
            while True:
                inputNumber = self.inputs.get_int()
                if 1 <= inputNumber <= 10:
                    break
                else:
                    print("Invalid input. Please enter a number between 1 and 10.")

            for i in range(int(inputNumber)):

                print("Enter date (MM/DD/YY): ")
                date = self.inputs.get_date()
                print("Enter meal calories: ")
                calories = self.inputs.get_int()
                print("Enter meal protein: ")
                protein = self.inputs.get_int()
                print("Enter meal fat: ")
                fat = self.inputs.get_int()
                print("Enter meal carbs: ")
                carbs = self.inputs.get_int()
                print("Enter water # of pints: ")
                water = self.inputs.get_int()
                print("Enter alcohol # of drinks: ")
                alcohol = self.inputs.get_int()
                print("Enter food type: ")
                types_list = ["SMALL MEAL", "LARGE MEAL", "SNACK", "DESSERT", "DRINK"]
                food_type_choice = self.inputs.get_list_choice(types_list)

                data = {
                    "date": date,
                    "calories": calories,
                    "protein": protein,
                    "fat": fat,
                    "carbs": carbs,
                    "water": water,
                    "alcohol": alcohol,
                    "food_type": food_type_choice
                }
                try:
                    self.db.insert(data)
                    print("Record inserted")
                except Exception as e:
                    print(e)
                    print("Error inserting data into database")

        except KeyboardInterrupt:
            print("Exiting...")
            print("")
            return
        except Exception as e:
            print(e)
            print("Error collecting data")
        
        self.displayData()
