from dataController.journals.timeKeeper import TimeKeeper
from dataController.journals.journal import Journal
from dataController.journals.nutrition import Nutrition
from dataController.journals.exercise import Exercise
from dataController.journals.sleep import Sleep
from dataController.journals.assets import Assets
from dataController.journals.liabilities import Liabilities
from dataController.functions.mongo import MongoDB
from colorama import Style, Fore
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
import bcrypt
import getpass
import os

timeKeeper = TimeKeeper()
journal = Journal()
sleep = Sleep()
exercise = Exercise()
nutrition = Nutrition()
assets = Assets()
liabilities = Liabilities()
mongo = MongoDB("admin")

def process_data(data_class):
    print(f"{data_class.__name__} selected...")
    print("Recent Data: ")
    data_class.displayData()
    while True:
        user_choice = input(Fore.BLUE + "(1)Insert, (2)Delete, (3)Update, (4)List By Date Range, (5)List All Data, (6)Display Single Date, (7)Exit: (1/2/3/4/5/6/7): " + Style.RESET_ALL)
        if user_choice == "1":
            data_class.collectData()
        elif user_choice == "2":
            data_class.deleteData()
        elif user_choice == "3":
            data_class.updateData()
        elif user_choice == "4":
            data_class.filterData()
        elif user_choice == "5":
            data_class.displayAllData()
        elif user_choice == "6":
            data_class.displaySingleDate()
        elif user_choice == "7":
            print("")
            print(f"Exiting {data_class.__name__}...")
            print("")
            break
        elif user_choice.lower() == "clear":
            clear_screen()
        else:
            print("Invalid input")

def process_finance_data(data_class):
    print(f"{data_class.__name__} selected...")
    print("Recent Data: ")
    data_class.displayAllData()
    while True:
        user_choice = input(Fore.BLUE + "(1)Insert, (2)Delete, (3)Update, (4)Exit: (1/2/3/4): " + Style.RESET_ALL)
        if user_choice == "1":
            data_class.collectData()
        elif user_choice == "2":
            data_class.deleteData()
        elif user_choice == "3":
            data_class.updateData()
        # elif user_choice == "4":
        #     data_class.filterData()
        elif user_choice == "4":
            print("")
            print(f"Exiting {data_class.__name__}...")
            print("")
            break
        elif user_choice.lower() == "clear":
            clear_screen()
        else:
            print("Invalid input")

def authenticate_user(password):
    pw = mongo.get({"user": "Admin"})
    pw = list(pw)[0]["password"]

    if bcrypt.checkpw(password.encode("utf-8"), pw.encode("utf-8")):
        return True
    return False

def clear_screen():
    # Clear screen based on the operating system
    if os.name == 'posix':  # For Unix/Linux/Mac OS
        _ = os.system('clear')
    elif os.name == 'nt':   # For Windows
        _ = os.system('cls')

while True:
    userInput = input(Fore.GREEN + "(1)TimeKeeper, (2)Journal, (3)Health, (4)Finances, (5)Exit: (1/2/3/4/5): " + Style.RESET_ALL)
    if userInput == "1":
        process_data(timeKeeper)

    elif userInput == "2":
        process_data(journal)

    elif userInput == "3":
        while True:
            health_choice = input(Fore.BLUE + "(1)View Sleep, (2)View Exercise, (3)View Nutrition, (4)Exit: (1/2/3/4): " + Style.RESET_ALL)
            if health_choice == "1":
                process_data(sleep)
            elif health_choice == "2":
                process_data(exercise)
            elif health_choice == "3":
                process_data(nutrition)
            elif health_choice == "4":
                print("")
                print("Exiting Health...")
                print("")
                break
            else:
                print("Invalid input")

    elif userInput == "4":
        password = getpass.getpass("Enter the password: ")
        if authenticate_user(password):
            while True:
                finance_choice = input(Fore.BLUE + "(1)View Assets, (2)View Liabilities, (3)View Bank Transactions (4)Exit: (1/2/3/4): " + Style.RESET_ALL)
                if finance_choice == "1":
                    process_finance_data(assets)
                elif finance_choice == "2":
                    process_finance_data(liabilities)
                elif finance_choice == "3":
                    print("Bank Transactions not yet implemented")
                elif finance_choice == "4":
                    print("")
                    print("Exiting Finances...")
                    print("")
                    break
        else:
            print("Incorrect password. Access Denied")
    elif userInput == "5":
        print("")
        print("Exiting...")
        print("")
        timeKeeper.close()
        journal.close()
        sleep.close()
        exercise.close()
        nutrition.close()
        exit()
    else:
        print("TimeKeeper, Journal, Health, or Exit")
