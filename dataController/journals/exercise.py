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

class Exercise:
    __name__ = "Exercise"

    def __init__(self):
        self.db = MongoDB("exercise")
        self.delete = Delete("exercise")
        self.display = Display("exercise")
        self.filter = Filter("exercise")
        self.display_all = DisplayAll("exercise")
        self.display_date = DisplayDate("exercise")
        self.update = Update("exercise")
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
            print("Enter number of exercises to enter: ")
            inputNumber = self.inputs.get_int()
            print("Enter date below:")
            date = self.inputs.get_date()
            
            for i in range(int(inputNumber)):

                print("Enter exercise type below:")
                type_list = ["RUNNING", "LIFTING", "STRETCHING", "FIGHTING", "SPORTS", "JUMP ROPE", "STAIRS/HIKING", "BODY/LIGHTWEIGHT CIRCUIT"]
                exercise_choice = self.inputs.get_list_choice(type_list)
                print("Enter duration below:")
                duration = self.inputs.get_float()
                print("Enter effort below:")
                effort = self.inputs.get_int()
                print("Enter reps below:")
                reps = self.inputs.get_int()
                print("Enter weight below:")
                weight = self.inputs.get_int()
                print("Enter distance below:")
                distance = self.inputs.get_float()
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


