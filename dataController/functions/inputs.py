import datetime
from datetime import date, timedelta

class Inputs:    
    def get_date(self):
        try:
            while True:
                date_start = input("")
                try:
                    parsed_start_date = datetime.datetime.strptime(date_start, "%m/%d/%y")
                    break
                except ValueError:
                    print("Incorrect data format, should be MM/DD/YY")
            return parsed_start_date
        except Exception as e:
            print(e)
            print("Error getting date")

    def get_time(self):
        try:
            while True:
                time_start = input("")
                try:
                    parsed_start_time = datetime.datetime.strptime(time_start, "%H:%M")
                    break
                except ValueError:
                    print("Incorrect data format, should be HH:MM")
            return parsed_start_time
        except Exception as e:
            print(e)
            print("Error getting time")

    def get_float(self):
        try:
            while True:
                value = input("")
                try:
                    value = float(value)
                    break
                except ValueError:
                    print("Invalid input")
            return value
        except Exception as e:
            print(e)
            print("Error getting float")
    
    def get_int(self):
        try:
            while True:
                value = input("")
                try:
                    value = int(value)
                    break
                except ValueError:
                    print("Invalid input")
            return value
        except Exception as e:
            print(e)
            print("Error getting int")  

    def get_list_choice(self, list):
        try:
            while True:
                for i in range(len(list)):
                    print(f"{i+1}: {list[i]}")
                choice = input("Enter choice #: ")
                try:
                    choice = int(choice)
                    if choice > 0 and choice <= len(list):
                        choice = list[choice-1]
                        break
                    else:
                        print("Invalid input")
                except ValueError:
                    print("Invalid input")
            return choice
        except Exception as e:
            print(e)
            print("Error getting list choice")