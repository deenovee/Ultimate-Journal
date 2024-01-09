from dataController.journals.timeKeeper import TimeKeeper
from dataController.journals.journal import Journal
from dataController.journals.nutrition import Nutrition
from dataController.journals.exercise import Exercise
from dataController.journals.sleep import Sleep
from dataController.health import Health
from colorama import Style, Fore

timeKeeper = TimeKeeper()
journal = Journal()
health = Health()
sleep = Sleep()
exercise = Exercise()
nutrition = Nutrition()


def process_tk_summary_data(data_class):
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

def process_health_data(data_class, choice):
    print(f"{data_class.__name__} selected...")
    print("Recent Data: ")
    data_class.displayData()

    while True:
        user_choice = input(Fore.BLUE + "(1)Insert, (2)Delete, (3)Update, (4)List By Date Range, (5)List All Data, (6)Display Single Date, (7)Exit: (1/2/3/4/5/6/7): " + Style.RESET_ALL)

        if user_choice == "1":
            data_class.collectData(choice)
        elif user_choice == "2":
            data_class.deleteData(choice)
        elif user_choice == "3":
            data_class.updateData(choice)
        elif user_choice == "4":
            data_class.filterData(choice)
        elif user_choice == "5":
            data_class.displayAllData(choice)
        elif user_choice == "6":
            data_class.displaySingleDate(choice)
        elif user_choice == "7":
            print("")
            print(f"Exiting {data_class.__name__}...")
            print("")
            break
        else:
            print("Invalid input")

while True:
    userInput = input(Fore.GREEN + "(1)TimeKeeper, (2)Journal, (3)Health, (4)Finances, (5)Exit: (1/2/3/4/5): " + Style.RESET_ALL)

    if userInput == "1":
        process_tk_summary_data(timeKeeper)

    elif userInput == "2":
        process_tk_summary_data(journal)

    elif userInput == "3":
        print("Health selected...")
        while True:
            health_choice = input(Fore.BLUE + "(1)View Sleep, (2)View Exercise, (3)View Nutrition, (4)Exit: (1/2/3/4): " + Style.RESET_ALL)
            if health_choice == "1":
                process_health_data(sleep, health_choice)
            elif health_choice == "2":
                process_health_data(exercise, health_choice)
            elif health_choice == "3":
                process_health_data(nutrition, health_choice)
            elif health_choice == "4":
                print("")
                print("Exiting Health...")
                print("")
                break
            else:
                print("Invalid input")

    elif userInput == "4":
        print("Finances selected...")
    
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
