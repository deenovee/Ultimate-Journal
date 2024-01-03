import pymongo
import datetime
from datetime import date, timedelta
from bson import ObjectId

class Nutrition:
    def __init__(self):
        try:
            self.client = pymongo.MongoClient("mongodb://localhost:27017/")
            self.db = self.client["MyDashboard"]
            self.collection = self.db["nutrition"]
        except pymongo.errors.ConnectionFailure as e:
            print(f"Failed to connect to MongoDB: {e}")

    def insert(self, data):
        try:
            self.collection.insert_one(data)
        except pymongo.errors.PyMongoError as e:
            print(f"Failed to insert document: {e}")

    def get(self, query):
        try:
            return self.collection.find(query)
        except pymongo.errors.PyMongoError as e:
            print(f"MongoDB query failed: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def get_by_id(self, id):
        try:
            return self.collection.find_one({"_id": ObjectId(id['_id'])})
        except pymongo.errors.PyMongoError as e:
            print(f"MongoDB query failed: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def delete(self, data):
        if "/" in data["_id"]:
            try:
                objectIds = data["_id"].split("/")
                for i in objectIds:
                    query = {"_id": ObjectId(i)}
                    self.collection.delete_one(query)
                    print("Record deleted")
            except Exception as e:
                print(e)
                print("Error handling multpiple ids")
                print("trying single id")
        else:
            query = {"_id": ObjectId(data["_id"])}
            try:
                self.collection.delete_one(query)
                print("Record deleted")
            except Exception as e:
                print(e)
                print("Error deleting data from database")
    
    def update(self, query, update_query):
        try:
            print("Updating...")
            self.collection.update_one(query, update_query)
            print("Record updated")
        except Exception as e:
            print(e)
            print("Error updating data in database")
    
    def close(self):
        self.client.close()

    def displayData(self):
        start_date = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=8)
        # Define the query to filter records within the date range
        query = {
            "date": {
                "$gte": start_date,
            }
        }
        try:
            nutrition_records = list(self.get(query))
        except pymongo.errors.PyMongoError as e:
            print(f"MongoDB query failed: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        
        if nutrition_records == []:
            print("No nutrition data for the past week")
        else:
            print("Nutrition Weekly Overview \n")
            for index, i in enumerate(nutrition_records):
                j = index + 1
                if j == len(nutrition_records):
                    print("")
                    print(f"Record {j}:\n _id = {i['_id']}\ndate = {i['date']}\nCalories = {i['calories']}\nProtein = {i['protein']}\nFat = {i['fat']}\nCarbs = {i['carbs']}\nWater = {i['water']}\nAlcohol = {i['alcohol']}\nFood Type = {i['food_type']}")
                    print("")
                else:
                    print("")
                    print(f"Record {j}:\n _id = {i['_id']}\ndate = {i['date']}\nCalories = {i['calories']}\nProtein = {i['protein']}\nFat = {i['fat']}\nCarbs = {i['carbs']}\nWater = {i['water']}\nAlcohol = {i['alcohol']}\nFood Type = {i['food_type']}")

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
                    water = input("Enter water: ")
                    try:
                        water = int(water)
                        break
                    except ValueError:
                        print("Invalid input")
                while True:
                    alcohol = input("Enter alcohol (y/n): ")
                    if alcohol == "y":
                        alcohol = True
                        break
                    elif alcohol == "n":
                        alcohol = False
                        break
                    else:
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
                    self.insert(data)
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

    def deleteData(self):
        try:
            existingData = list(self.get({}))
        except Exception as e:
            print("Error retrieving data from database")
        if existingData:
            try:
                while True:
                    id = input("Enter Object ID to delete or list of IDs separated by /: ")
                    try:
                        id = str(id)
                        break
                    except ValueError:
                        print(ValueError)
                query = {"_id": id}
                try:
                    self.delete(query)
                    print("Exercise data deleted successfully")
                except pymongo.errors.PyMongoError as e:
                    print(f"Failed to delete document: {e}")
                except Exception as e:
                    print(f"An error occurred: {e}")
            except KeyboardInterrupt:
                print("")
                print("Exiting...")
                print("")
            self.displayData()
        else:
            print("No data to delete")
            print("Exiting...\n")

    def updateData(self):
        try:
            existingData = list(self.get({}))
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
            objectToUpdate = self.get_by_id(idToUpdate)
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
                self.update(query, update_query)
            except Exception as e:
                print(e)
                print("Error updating data from database\n")

            self.displayData()
        else:
            print("No data to update")
            print("Exiting...\n")

    def filterData(self):
        try:
            existingData = list(self.get({}))
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
                filteredData = list(self.get(query))
            except Exception as e:
                print(e)
                print("Error retrieving data from database\n")

            if filteredData:
                for index, i in enumerate(filteredData):
                    j = index + 1
                    if j == len(filteredData):
                        print("")
                        print(f"Record {index + 1}:\n _id = {i['_id']}\ndate = {i['date']}\nCalories = {i['calories']}\nProtein = {i['protein']}\nFat = {i['fat']}\nCarbs = {i['carbs']}\nWater = {i['water']}\nAlcohol = {i['alcohol']}\nFood Type = {i['food_type']}")
                        print("")
                    else:
                        print("")
                        print(f"Record {index + 1}:\n _id = {i['_id']}\ndate = {i['date']}\nCalories = {i['calories']}\nProtein = {i['protein']}\nFat = {i['fat']}\nCarbs = {i['carbs']}\nWater = {i['water']}\nAlcohol = {i['alcohol']}\nFood Type = {i['food_type']}")
            else:
                print("No data found for that date range")
        else:
            print("No data to filter")
            print("Exiting...\n")

    def displayAllData(self):
        try:
            existingData = list(self.get({}))
        except Exception as e:
            print("Error retrieving data from database")
        if existingData:
            for index, i in enumerate(existingData):
                j = index + 1
                if j == len(existingData):
                    print("")
                    print(f"Record {index + 1}:\n _id = {i['_id']}\ndate = {i['date']}\nCalories = {i['calories']}\nProtein = {i['protein']}\nFat = {i['fat']}\nCarbs = {i['carbs']}\nWater = {i['water']}\nAlcohol = {i['alcohol']}\nFood Type = {i['food_type']}")
                    print("")
                else:
                    print("")
                    print(f"Record {index + 1}:\n _id = {i['_id']}\ndate = {i['date']}\nCalories = {i['calories']}\nProtein = {i['protein']}\nFat = {i['fat']}\nCarbs = {i['carbs']}\nWater = {i['water']}\nAlcohol = {i['alcohol']}\nFood Type = {i['food_type']}")
        else:
            print("No data to display")
            print("Exiting...\n")

    def displaySingleDate(self):
        try:
            existingData = list(self.get({}))
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
                filteredData = list(self.get(query))
            except Exception as e:
                print(e)
                print("Error retrieving data from database\n")
            if filteredData:
                for index, i in enumerate(filteredData):
                    j = index + 1 
                    if j == len(filteredData):
                        print("")
                        print(f"Record {index + 1}:\n _id = {i['_id']}\ndate = {i['date']}\nCalories = {i['calories']}\nProtein = {i['protein']}\nFat = {i['fat']}\nCarbs = {i['carbs']}\nWater = {i['water']}\nAlcohol = {i['alcohol']}\nFood Type = {i['food_type']}")
                        print("")
                    else:
                        print("")
                        print(f"Record {index + 1}:\n _id = {i['_id']}\ndate = {i['date']}\nCalories = {i['calories']}\nProtein = {i['protein']}\nFat = {i['fat']}\nCarbs = {i['carbs']}\nWater = {i['water']}\nAlcohol = {i['alcohol']}\nFood Type = {i['food_type']}")
            else:
                print("No data to display")