from dataController.journals.timeKeeper import TimeKeeper
from dataController.journals.journal import Journal
from dataController.journals.nutrition import Nutrition
from dataController.journals.exercise import Exercise
from dataController.journals.sleep import Sleep
from dataController.journals.assets import Assets
from dataController.journals.liabilities import Liabilities
from dataController.journals.bank1 import BANK1
from dataController.journals.bank2 import BANK2
from dataController.functions.mongo import MongoDB
from colorama import Style, Fore
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
import bcrypt
import getpass
import os
from dotenv import load_dotenv

timeKeeper = TimeKeeper()
journal = Journal()
sleep = Sleep()
exercise = Exercise()
nutrition = Nutrition()
assets = Assets()
liabilities = Liabilities()
bank_1_class = BANK1()
bank_2_class = BANK2()
mongo = MongoDB("admin")
load_dotenv()
bank_1 = os.getenv("BANK_1")
bank_2 = os.getenv("BANK_2")

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
            data_class.close()
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
            data_class.close()
            break
        elif user_choice.lower() == "clear":
            clear_screen()
        else:
            print("Invalid input")

def process_bank_data(data_class):
    print(f"{data_class.__name__}")
    while True:
        user_choice = input(Fore.BLUE + "(1)Insert, (2)Delete, (3)Display Last 7 Days, (4)List By Date Range, (5)Exit: (1/2/3/4/5): " + Style.RESET_ALL)
        if user_choice == "1":
            data_class.collectData()
        elif user_choice == "2":
            data_class.deleteData()
        elif user_choice == "3":
            data_class.displayData()
        elif user_choice == "4":
            data_class.filterData()
        elif user_choice == "5":
            print("")
            print(f"Exiting {data_class.__name__}...")
            print("")
            data_class.close()
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
    if os.name == 'posix':
        _ = os.system('clear')
    elif os.name == 'nt':
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
                    bank_choice = input(Fore.MAGENTA + f"(1){bank_1}, (2){bank_2} (3)Exit (1/2/3): " + Style.RESET_ALL )
                    if bank_choice == '1':
                        process_bank_data(bank_1_class)
                    if bank_choice == '2':
                        process_bank_data(bank_2_class)
                    if bank_choice == '3':
                        print("")
                        print("Exiting Bank Transactions...")
                        print("")
                        break
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
    elif userInput.lower() == "clear":
        clear_screen()
    else:
        print("TimeKeeper, Journal, Health, or Exit")
