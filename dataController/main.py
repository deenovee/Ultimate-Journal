from timeKeeper import TimeKeeper
from journal import Journal
from health import Health
from colorama import Style, Fore

#instantiate TimeKeeper class
timeKeeper = TimeKeeper()
#instantiate Journal class
journal = Journal()
#instantiate Health class
health = Health()

#keep prompting user until they choose 1, 2, 3, 4
while True:
    #get user input
    userInput = input(Fore.GREEN + "(1)TimeKeeper, (2)Journal, (3)Health, (4)Finances, (5)Exit: (1/2/3/4/5): " + Style.RESET_ALL)

    #validate user input
    if userInput == "1":
        print("TimeKeeper selected...")
        print("Recent Data: ")
        timeKeeper.displayData()
        while True:
            tk_choice = input(Fore.BLUE + "(1)Insert, 2(Delete), (3)Update, (4)List By Date, (5)List All Data, (6)Exit: (1/2/3/4/5/6): " + Style.RESET_ALL)
            if tk_choice == "1":
                timeKeeper.collectData()
            elif tk_choice == "2":
                timeKeeper.deleteData()
            elif tk_choice == "3":
                timeKeeper.updateData()
            elif tk_choice == "4":
                timeKeeper.filterData()
            elif tk_choice == "5":
                timeKeeper.displayAllData()
            elif tk_choice == "6":
                print("")
                print("Exiting TimeKeeper...")
                print("")
                break
            else:
                print("Invalid input")

    elif userInput == "2":
        print("Journal selected...")
        print("Last Entry: ")
        journal.displayRecentJournal()
        while True:
            journal_choice = input(Fore.BLUE + "(1)Insert, 2(Delete), (3)Update, (4)List By Date Range, (5)List All Data, (6)Exit: (1/2/3/4/5/6): " + Style.RESET_ALL)
            if journal_choice == "1":
                journal.collectData()
            elif journal_choice == "2":
                journal.deleteData()
            elif journal_choice == "3":
                journal.updateData()
            elif journal_choice == "4":
                journal.filterData()
            elif journal_choice == "5":
                journal.displayAllData()
            elif journal_choice == "6":
                print("")
                print("Exiting Journal...")
                print("")
                break
            else:
                print("Invalid input")

    elif userInput == "3":
        print("Health selected...")
        while True:
            health_choice = input(Fore.BLUE + "(1)View Sleep, (2)View Exercise, (3)View Nutrition, (4)Exit: (1/2/3/4): " + Style.RESET_ALL)
            if health_choice == "1":
                health.sleep_dash()
                while True:
                    sleep_choice = input(Fore.MAGENTA + "(1)Insert, (2)Delete, (3)Update, (4)List By Date Range, (5)List All Data, (6)Exit: (1/2/3/4/5/6): " + Style.RESET_ALL)
                    if sleep_choice == "1":
                        health.insert_sleep_doc()
                    elif sleep_choice == "2":
                        health.delete_sleep_doc()
                    elif sleep_choice == "3":
                        health.update_sleep_doc()
                    elif sleep_choice == "4":
                        health.filter_sleep_data()
                    elif sleep_choice == "5":
                        health.display_all_sleep_data()
                    elif sleep_choice == "6":
                        print("")
                        print("Exiting Sleep...")
                        print("")
                        break
                    else:
                        print("Invalid input")
            elif health_choice == "2":
                health.exercise_dash()
                while True:
                    exercise_choice = input(Fore.MAGENTA + "(1)Insert, (2)Delete, (3)Update, (4)List By Date Range, (5)List All Data, (6)Exit: (1/2/3/4/5/6): " + Style.RESET_ALL)
                    if exercise_choice == "1":
                        health.insert_exercise_doc()
                    elif exercise_choice == "2":
                        health.delete_exercise_doc()
                    elif exercise_choice == "3":
                        health.update_exercise_doc()
                    elif exercise_choice == "4":
                        health.filter_exercise_data()
                    elif exercise_choice == "5":
                        health.display_all_exercise_data()
                    elif exercise_choice == "6":
                        print("")
                        print("Exiting Exercise...")
                        print("")
                        break
                    else:
                        print("Invalid input")
            elif health_choice == "3":
                health.nutrition_dash()
                while True:
                    nutrition_choice = input(Fore.MAGENTA + "(1)Insert, (2)Delete, (3)Update, (4)List By Date Range, (5)List All Data, (6)Exit: (1/2/3/4/5/6): " + Style.RESET_ALL)
                    if nutrition_choice == "1":
                        health.insert_nutrition_doc()
                    elif nutrition_choice == "2":
                        health.delete_nutrition_doc()
                    elif nutrition_choice == "3":
                        health.update_nutrition_doc()
                    elif nutrition_choice == "4":
                        health.filter_nutrition_data()
                    elif nutrition_choice == "5":
                        health.display_all_nutrition_data()
                    elif nutrition_choice == "6":
                        print("")
                        print("Exiting Nutrition...")
                        print("")
                        break
                    else:
                        print("Invalid input")
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
        #close database connections
        timeKeeper.close()
        journal.close()
        #exit program
        exit()

    else:
        #prompt user to choose from 1, 2 or 3
        print("TimeKeeper, Journal, Health, or Exit")
