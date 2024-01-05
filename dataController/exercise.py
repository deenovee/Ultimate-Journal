from mongo import MongoDB
import datetime
from datetime import date, timedelta
from bson import ObjectId

class Exercise:
    def __init__(self):
        self.db = MongoDB("exercise")

    def close(self):
        self.db.close()

    def displayData(self):
        start_date = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=8)  # Adjust the number of days as needed

        # Define the query to filter records within the date range
        query = {
            "date": {
                "$gte": start_date
            }
        }
        try:
            exercise_records = list(self.db.get(query))
        except pymongo.errors.PyMongoError as e:
            print(f"Failed to retrieve data from MongoDB: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

        if exercise_records == []:
            print("No exercise data for the past week")
        else:
            print("Exercise Weekly Overview: \n")

            # display sleep data 
            for index, i in enumerate(exercise_records):
                j = index + 1
                if j == len(exercise_records):
                    print("")
                    print(f"Record {j}: \n _id = {i['_id']}\n date = {i['date']}\n exercise_type = {i['exercise_type']}\n duration = {i['duration']} minutes\n effort = {i['effort']}\n reps = {i['reps']}\n weight = {i['weight']}\n distance = {i['distance']} miles\n description = {i['description']}")
                    print("")
                else:
                    print("")
                    print(f"Record {j}: \n _id = {i['_id']}\n date = {i['date']}\n exercise_type = {i['exercise_type']}\n duration = {i['duration']} minutes\n effort = {i['effort']}\n reps = {i['reps']}\n weight = {i['weight']}\n distance = {i['distance']} miles\n description = {i['description']}")

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
                    date = input("Enter date (mm/dd/yy): ")
                    try:
                        date = datetime.datetime.strptime(date, '%m/%d/%y')
                        break
                    except ValueError:
                        print("Incorrect date format, should be mm/dd/yy")

                type_list = ["RUNNING", "LIFTING", "STRETCHING", "FIGHTING", "SPORTS", "JUMP ROPE", "STAIRS/HIKING", "BODY/LIGHTWEIGHT CIRCUIT"]
                for i in range(len(type_list)):
                    print(f"{i+1}. {type_list[i]}") 
                while True:   
                    try:    
                        exercise_type = input("Enter exercise type: ")
                        exercise_type = int(exercise_type)
                        exercise_choice = type_list[exercise_type-1]
                        break
                    except ValueError:
                        print("Invalid input")

                while True:    
                    duration = input("Enter duration (minutes): ")
                    try:
                        duration = int(duration)
                        break
                    except ValueError:
                        print("Invalid input")

                while True:    
                    effort = input("Enter effort (1-10): ")
                    try:
                        effort = int(effort)
                        break
                    except ValueError:
                        print("Invalid input")
                
                while True:    
                    reps = input("Enter reps: ")
                    try:
                        reps = int(reps)
                        break
                    except ValueError:
                        print("Invalid input")
                
                while True:    
                    weight = input("Enter weight: ")
                    try:
                        weight = int(weight)
                        break
                    except ValueError:
                        print("Invalid input")
                
                while True:    
                    distance = input("Enter distance (miles): ")
                    try:
                        distance = float(distance)
                        break
                    except ValueError:
                        print("Invalid input")
                
                while True:    
                    description = input("Enter description: ")
                    try:
                        description = str(description)
                        break
                    except ValueError:
                        print("Invalid input")

                data = {
                    "date": date,
                    "exercise_type": exercise_choice,
                    "duration": duration,
                    "effort": effort,
                    "reps": reps,
                    "weight": weight,
                    "distance": distance,
                    "description": description
                }

                try:
                    self.db.insert(data)
                    print("Exercise data inserted successfully")
                except pymongo.errors.PyMongoError as e:
                    print(f"Failed to insert document: {e}")
                except Exception as e:
                    print(f"An error occurred: {e}")
        except KeyboardInterrupt:
            print("")
            print("Exiting...")
            print("")
        except Exception as e:
            print(e)
            print("Error inserting data into database")

        self.displayData()

    def deleteData(self):
        try:
            existingData = list(self.db.get({}))
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
                    self.db.delete(query)
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
            print("Exiting...")


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
            
            while True:
                newValue = input("Enter new value: ")
                if newValue:
                    query_data = {"_id": ObjectId(id)}
                    new_values = {"$set": {f"{selectedKey}": newValue}}
                    break
                else:
                    print("Invalid input try again.")
            
            try:
                self.db.update(query_data, new_values)
            except Exception as e:
                print(e)
                print("Error updating data in database\n")

            self.displayData()

        else:
            print("No data to update")
            print("Exiting...")

    def filterData(self):
        try:
            existingData = list(self.db.get({}))
        except Exception as e:
            print("Error retrieving data from database")
        
        if existingData:
            while True:
                try:
                    start_date = input("Enter start date (mm/dd/yy): ")
                    start_date = datetime.datetime.strptime(start_date, '%m/%d/%y')
                    break
                except ValueError:
                    print("Incorrect date format, should be mm/dd/yy")
            while True:
                try:
                    end_date = input("Enter end date (mm/dd/yy): ")
                    end_date = datetime.datetime.strptime(end_date, '%m/%d/%y')
                    break
                except ValueError:
                    print("Incorrect date format, should be mm/dd/yy")
            query = {
                "date": {
                    "$gte": start_date,
                    "$lte": end_date
                }
            }
            try:
                filteredData = list(self.db.get(query))
            except Exception as e:
                print("Error filtering data")
            
            if filteredData:
                for index, i in enumerate(filteredData):
                    j = index + 1  
                    if j == len(filteredData):
                        print("")
                        print(f"Record {j}:\n _id = {i['_id']}\n date = {i['date']}\n exercise_type = {i['exercise_type']}\n duration = {i['duration']} minutes\n effort = {i['effort']}\n reps = {i['reps']}\n weight = {i['weight']}\n distance = {i['distance']} miles\n description = {i['description']}")
                        print("")
                    else:
                        print("")
                        print(f"Record {j}:\n _id = {i['_id']}\n date = {i['date']}\n exercise_type = {i['exercise_type']}\n duration = {i['duration']} minutes\n effort = {i['effort']}\n reps = {i['reps']}\n weight = {i['weight']}\n distance = {i['distance']} miles\n description = {i['description']}")
            else:
                print("No data found for that date range.")
        else:
            print("No data to filter")
            print("Exiting...\n")

    def displayAllData(self):
        try:
            existingData = list(self.db.get({}))
        except Exception as e:
            print("Error retrieving data from database")
        if existingData:
            for index, i in enumerate(existingData):
                j = index + 1  
                if j == len(existingData):
                    print("")
                    print(f"Record {j}:\n _id = {i['_id']}\n date = {i['date']}\n exercise_type = {i['exercise_type']}\n duration = {i['duration']} minutes\n effort = {i['effort']}\n reps = {i['reps']}\n weight = {i['weight']}\n distance = {i['distance']} miles\n description = {i['description']}")
                    print("")
                else:
                    print("")
                    print(f"Record {j}:\n _id = {i['_id']}\n date = {i['date']}\n exercise_type = {i['exercise_type']}\n duration = {i['duration']} minutes\n effort = {i['effort']}\n reps = {i['reps']}\n weight = {i['weight']}\n distance = {i['distance']} miles\n description = {i['description']}")
        else:
            print("No data to display")
            print("Exiting...\n")

    def displaySingleDate(self):
        try:
            existingData = list(self.db.get({}))
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
                filteredData = list(self.db.get(query))
            except Exception as e:
                print(e)
                print("Error retrieving data from database\n")
            if filteredData:
                for index, i in enumerate(filteredData):
                    j = index + 1 
                    if j == len(filteredData):
                        print("")
                        print(f"Record {j}:\n _id = {i['_id']}\n date = {i['date']}\n exercise_type = {i['exercise_type']}\n duration = {i['duration']} minutes\n effort = {i['effort']}\n reps = {i['reps']}\n weight = {i['weight']}\n distance = {i['distance']} miles\n description = {i['description']}")
                        print("")
                    else:
                        print("")
                        print(f"Record {j}:\n _id = {i['_id']}\n date = {i['date']}\n exercise_type = {i['exercise_type']}\n duration = {i['duration']} minutes\n effort = {i['effort']}\n reps = {i['reps']}\n weight = {i['weight']}\n distance = {i['distance']} miles\n description = {i['description']}")
            else:
                print("No data to display")