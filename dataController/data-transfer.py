from datetime import datetime, timedelta
import pymongo
import colorama
from colorama import Fore, init


init(autoreset=True)
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
database = mongo_client["MyDashboard"]


def tk_data_transfer():
    collection = database["timeKeeper"]

    with open('./data.txt', 'r') as file:
        input_data = file.read()

    documents_list = []

    counter = 0
    for line in input_data.strip().split('\n'):
        counter += 1
        print(f"Record #{counter}")
        try:
            date_str, rest = map(str.strip, line.split('-', 1))
            iso_date = datetime.strptime(date_str, "%m/%d/%y")
            entries = rest.split(', ')
            for entry in entries:
                time = []
                for i, char in enumerate(entry):
                    if char == ' ':
                        entry = entry[i:]
                        break
                    else:
                        time.append(str(char))

                time = int(''.join(time))

                category = int(entry[-1])
                desc = entry[:-1].strip()

                document = {
                    "date": iso_date,
                    "time": time,
                    "description": desc,
                    "category": category
                }
                print(Fore.GREEN + f"Document #{counter}: {document}")
                print("\n")
                documents_list.append(document)
        except Exception as e:
            print (Fore.RED + f"Error processing record #{counter}: {line}")
            print(e)
    collection.insert_many(documents_list)

def sleep_data_transfer():
    collection = database['sleep']
    with open('./data.txt', 'r') as file:
        input_data = file.read()

    documents_list = []

    counter = 0
    for line in input_data.strip().split('\n'):
        counter += 1
        # print(f"Record #{counter}")
        # print(line + '\n\n')  
        try:
            start_date_str, end_date_str, nap, quality = map(str.strip, line.split('-', 3))
            formatted_start_date = datetime.strptime(start_date_str.split(' ')[0], "%m/%d/%y")
            formatted_start_time = datetime.strptime(start_date_str.split(' ')[1], "%H:%M")
            formatted_end_date = datetime.strptime(end_date_str.split(' ')[0], "%m/%d/%y")
            formatted_end_time = datetime.strptime(end_date_str.split(' ')[1], "%H:%M")

            start_date = datetime.combine(formatted_start_date, formatted_start_time.time())
            end_date = datetime.combine(formatted_end_date, formatted_end_time.time())

            if nap == 'y':
                nap = True
            else:
                nap = False

            hours = end_date - start_date
            document = {
                "time_start": start_date,
                "time_end": end_date,
                "hours": hours.seconds / 3600,
                "nap": nap,
                "quality": int(quality)
            }

            print(Fore.GREEN + f"Document #{counter}: {document}")
            print("\n")
            documents_list.append(document)
            # print(start_date)
            # print(end_date)
            # print(nap + '\n' + quality)

        except Exception as e:
            print (Fore.RED + f"Error processing record #{counter}: {line}")
            print(e)

    collection.insert_many(documents_list)

def nutrition_data_transfer():
    collection = database['nutrition']
    with open('./data.txt', 'r') as file:
        input_data = file.read()

    documents_list = []

    counter = 0
    date = datetime.strptime('11/1/23', "%m/%d/%y")
    for line in input_data.strip().split('\n'):
        counter += 1
        print(f"Record #{counter}")
        try:
            document = {
                "date": date,
                "calories": 0,
                "protein": 0,
                "fat": 0,
                "carbs": 0,
                "water": int(line),
                "alcohol": 0,
                "food_type": "DRINK"
            }
            print(Fore.GREEN + f"Document #{counter}: {document}\n")
            documents_list.append(document)
            date = date + timedelta(days=1)
        except Exception as e:
            print (Fore.RED + f"Error processing record #{counter}: {line}")
            print(e)

    collection.insert_many(documents_list)

     

mongo_client.close()
