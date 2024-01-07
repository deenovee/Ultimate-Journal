from .mongo import MongoDB
from .display import Display
from bson import ObjectId
import datetime
from datetime import date, timedelta

class Update:
    def __init__(self, collection):
        self.db = MongoDB(collection)
        self.collection = collection
        self.display = Display(collection)
        self.meal_types = ["SMALL MEAL", "LARGE MEAL", "SNACK", "DESSERT", "DRINK"]
        self.exercise_types = ["RUNNING", "LIFTING", "STRETCHING", "FIGHTING", "SPORTS", "JUMP ROPE", "STAIRS/HIKING", "BODY/LIGHTWEIGHT CIRCUIT"]
        self.tk_categories = ['HEALTH', 'WORK', 'PROJECT', 'EDUCATION', 'READING', 'HOBBY', 'NETWORKING', 'OTHER']
    
    def calculate_hours(self, date_time1, date_time2):
        try:
            if not isinstance(date_time1, datetime.datetime) or not isinstance(date_time2, datetime.datetime):
                raise ValueError("Input times must be datetime.datetime objects")
            difference = date_time2 - date_time1
            hours = difference.total_seconds() / 3600
            return hours
        except ValueError:
            print("Incorrect data format, should be HH:MM")
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def update(self):
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

            if selectedKey == "date":
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

            elif selectedKey == "time_start" or selectedKey == "time_end":
                while True:
                    new_time= input("Enter new time value (HH:MM): ")
                    try:
                        new_time = datetime.datetime.strptime(new_time, "%H:%M").time()
                        break
                    except ValueError:
                        print("Incorrect data format, should be HH:MM")
                while True:
                    new_date = input("Enter new date value (MM/DD/YY): ")
                    try:
                        new_date = datetime.datetime.strptime(new_date, "%m/%d/%y").date()
                        break
                    except ValueError:
                        print("Incorrect data format, should be MM/DD/YY")
                combined_datetime = datetime.datetime.combine(new_date, new_time)
                try:
                    query = {"_id": ObjectId(id)}
                    update_query = {"$set": {f"{selectedKey}": combined_datetime}}
                except pymongo.errors.PyMongoError as e:
                    print(f"Error: {e}\nError updating data in database")
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")

            elif selectedKey == "calories" or selectedKey == "protein" or selectedKey == "carbs" or selectedKey == "fat" or selectedKey == "hours" or selectedKey == "quality" or selectedKey == "rating" or selectedKey == "duration" or selectedKey == "effort" or selectedKey == "reps" or selectedKey == "weight" or selectedKey == "distance" or selectedKey == "time":
                while True:
                    newValue = input("Enter new value: ")
                    if newValue:
                        try:
                            newValue = float(newValue)
                            query = {"_id": ObjectId(id)}
                            update_query = {"$set": {f"{selectedKey}": newValue}}
                            break
                        except ValueError:
                            print("Invalid input, try again.")
                    else:
                        print("Invalid input, try again.")

            elif selectedKey == "water" or selectedKey == "alcohol":
                while True:
                    newValue = input("Enter new value (# of drinks): ")
                    if newValue:
                        try:
                            newValue = int(newValue)
                            query = {"_id": ObjectId(id)}
                            update_query = {"$set": {f"{selectedKey}": newValue}}
                            break
                        except ValueError:
                            print("Invalid input, try again.")
                    else:
                        print("Invalid input, try again.")

            elif selectedKey == "food_type":
                for index, i in enumerate(self.meal_types):
                    print(f"{index+1} - {i}")
                while True:
                    newValue = input("Enter new value: ")
                    if newValue:
                        try:
                            newValue = int(newValue)
                            if 1 <= newValue <= len(self.meal_types):
                                newValue = self.meal_types[newValue-1]
                                query = {"_id": ObjectId(id)}
                                update_query = {"$set": {f"{selectedKey}": newValue}}
                                break
                            else:
                                print("Invalid input, try again.")
                        except ValueError:
                            print("Invalid input, try again.")
                    else:
                        print("Invalid input, try again.")
            
            elif selectedKey == "exercise_type":
                for index, i in enumerate(self.exercise_types):
                    print(f"{index+1} - {i}")
                while True:
                    newValue = input("Enter new value: ")
                    if newValue:
                        try:
                            newValue = int(newValue)
                            if 1 <= newValue <= len(self.exercise_types):
                                newValue = self.exercise_types[newValue-1]
                                query = {"_id": ObjectId(id)}
                                update_query = {"$set": {f"{selectedKey}": newValue}}
                                break
                            else:
                                print("Invalid input, try again.")
                        except ValueError:
                            print("Invalid input, try again.")
                    else:
                        print("Invalid input, try again.")

            elif selectedKey == "category":
                for index, i in enumerate(self.tk_categories):
                    print(f"{index+1} - {i}")
                while True:
                    newValue = input("Enter new value: ")
                    if newValue:
                        try:
                            newValue = int(newValue)
                            if 1 <= newValue <= len(self.tk_categories):
                                newValue = self.tk_categories[newValue-1]
                                query = {"_id": ObjectId(id)}
                                update_query = {"$set": {f"{selectedKey}": newValue}}
                                break
                            else:
                                print("Invalid input, try again.")
                        except ValueError:
                            print("Invalid input, try again.")
                    else:
                        print("Invalid input, try again.")

            elif selectedKey == "nap":
                while True:
                    nap = input("Nap? (y/n): ")
                    try: 
                        nap = nap.lower()
                        if nap == "y":
                            nap = True
                            break
                        elif nap == "n":
                            nap = False
                            break
                        else:
                            print("Enter y or n")
                    except ValueError:
                        print("Invalid input")

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
                if selectedKey == "time_start":
                    hours = self.calculate_hours(combined_datetime, objectToUpdate["time_end"])
                    self.db.update(query, {"$set": {"hours": hours}})
                elif selectedKey == "time_end":
                    hours = self.calculate_hours(objectToUpdate["time_start"], combined_datetime)
                    self.db.update(query, {"$set": {"hours": hours}})
            except Exception as e:
                print(e)
                print("Error updating data from database\n")

            self.display.display()
        else:
            print("No data to update")
            print("Exiting...\n")    