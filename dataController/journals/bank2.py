from dataController.functions.mongo import MongoDB
from dataController.functions.delete import Delete
from dataController.functions.display import Display
from dataController.functions.filter import Filter
from dataController.functions.inputs import Inputs
import csv
import datetime
from datetime import date, timedelta
from dotenv import load_dotenv
import os



class BANK2:
    __name__: "Bank2"

    def __init__(self):
        load_dotenv()
        self.__name__ = "Bank2"
        self.inputs = Inputs()
        self.bank_2 = os.getenv("BANK_2")
        self.db = MongoDB(f"{self.bank_2}")
        self.delete = Delete(f"{self.bank_2}")
        self.display = Display(f"{self.bank_2}")
        self.filter = Filter(f"{self.bank_2}")
        

    def collectData(self):
        try:
            print("Enter the path of the file: ")
            path = Inputs().get_string()
            with open(path, 'r') as file:
                reader = csv.reader(file)
                new_list = []
                for row in reader:
                    modified_row = {
                        "transaction_date": datetime.datetime.strptime(row[0], "%m/%d/%Y"), 
                        "transaction_amount": row[1], 
                        "statement": row[4]
                    }
                    self.db.insert(modified_row)
            print("Data collected")
        except Exception as e:
            print(e)
            print("Error collecting data")
        except FileNotFoundError:
            print("File not found")
        
    def deleteData(self):
        try:
            self.delete.delete()
        except Exception as e:
            print(e)
            print("Error deleting data")
    
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

    def close(self):
        self.db.close()
