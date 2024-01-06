from functions.mongo import MongoDB
from functions.delete import Delete
from functions.display import Display
from functions.filter import Filter
from functions.display_all import DisplayAll
from functions.display_date import DisplayDate
import datetime
from datetime import date, timedelta
from bson import ObjectId

class Nutrition:
    def __init__(self):
        self.db = MongoDB("nutrition")
        self.delete = Delete("nutrition")
        self.display = Display("nutrition")
        self.filter = Filter("nutrition")
        self.display_all = DisplayAll("nutrition")
        self.display_date = DisplayDate("nutrition")
    
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

    def collectData(self):
        try:
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

            for i in range(int(inputNumber)):
                while True:
                    date_start = input("Enter date (MM/DD/YY): ")
                    try:
                        parsed_start_date = datetime.datetime.strptime(date_start, "%m/%d/%y")
                        break
                    except ValueError:
                        print("Incorrect data format, should be MM/DD/YY")

                while True:
                    calories = input("Enter meal calories: ")
                    try:
                        calories = int(calories)
                        break
                    except ValueError:
                        print("Invalid input")
                while True:
                    protein = input("Enter meal protein: ")
                    try:
                        protein = int(protein)
                        break
                    except ValueError:
                        print("Invalid input")
                while True:
                    fat = input("Enter meal fat: ")
                    try:
                        fat = int(fat)
                        break
                    except ValueError:
                        print("Invalid input")
                while True:
                    carbs = input("Enter meal carbs: ")
                    try:
                        carbs = int(carbs)
                        break
                    except ValueError:
                        print("Invalid input")
                while True:
                    water = input("Enter water # of pints: ")
                    try:
                        water = int(water)
                        break
                    except ValueError:
                        print("Invalid input")
                while True:
                    alcohol = input("Enter alcohol # of drinks: ")
                    try:
                        int(alcohol)
                        break
                    except ValueError:
                        print("Invalid input")
                while True:
                    types_list = ["SMALL MEAL", "LARGE MEAL", "SNACK", "DESSERT", "DRINK"]
                    for i in range(len(types_list)):
                        print(f"{i+1}: {types_list[i]}")

                    food_type = input("Enter food type: ")
                    try:
                        food_type = int(food_type)
                        if food_type > 0 and food_type <= len(types_list):
                            food_type_choice = types_list[food_type-1]
                            break
                        else:
                            print("Invalid input")
                    except ValueError:
                        print("Invalid input")

                data = {
                    "date": parsed_start_date,
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
                    if newValue:
                        try:
                            newValue = datetime.datetime.strptime(newValue, "%m/%d/%y")
                            query = {"_id": ObjectId(id)}
                            update_query = {"$set": {f"{selectedKey}": newValue}}
                            break
                        except ValueError:
                            print("Incorrect data format, should be MM/DD/YY")
                    else:
                        print("Invalid input try again.")
            else:
                while True:
                    newValue = input("Enter new value: ")
                    if newValue:
                        query = {"_id": ObjectId(id)}
                        update_query = {"$set": {f"{selectedKey}": newValue}}
                        break
                    else:
                        print("Invalid input try again.")

            #update data from database
            try:
                self.db.update(query, update_query)
            except Exception as e:
                print(e)
                print("Error updating data from database\n")

            self.displayData()
        else:
            print("No data to update")
            print("Exiting...\n")