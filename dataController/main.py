from dataController.journals.timeKeeper import TimeKeeper
from dataController.journals.journal import Journal
from dataController.journals.nutrition import Nutrition
from dataController.journals.exercise import Exercise
from dataController.journals.sleep import Sleep
from dataController.journals.assets import Assets
from dataController.journals.liabilities import Liabilities
from colorama import Style, Fore

timeKeeper = TimeKeeper()
journal = Journal()
sleep = Sleep()
exercise = Exercise()
nutrition = Nutrition()
assets = Assets()
liabilities = Liabilities()

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
        else:
            print("Invalid input")

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
        while True:
            fiance_choice = input(Fore.BLUE + "(1)View Assets, (2)View Liabilities, (3)View Bank Transactions (4)Exit: (1/2/3/4): " + Style.RESET_ALL)
            if fiance_choice == "1":
                process_finance_data(assets)
            elif fiance_choice == "2":
                process_finance_data(liabilities)
            elif fiance_choice == "3":
                print("Bank Transactions not yet implemented")
            elif fiance_choice == "4":
                print("")
                print("Exiting Finances...")
                print("")
                break
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
