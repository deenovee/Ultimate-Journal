from functions.mongo import MongoDB
from functions.delete import Delete
from functions.display import Display
from functions.filter import Filter
from functions.display_all import DisplayAll
from functions.display_date import DisplayDate
import datetime
from datetime import date, timedelta
from bson import ObjectId

class Exercise:
    def __init__(self):
        self.db = MongoDB("exercise")
        self.delete = Delete("exercise")
        self.display = Display("exercise")
        self.filter = Filter("exercise")
        self.display_all = DisplayAll("exercise")
        self.display_date = DisplayDate("exercise")

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
