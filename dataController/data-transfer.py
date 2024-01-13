from datetime import datetime
import pymongo
import colorama
from colorama import Fore, init


init(autoreset=True)
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
database = mongo_client["MyDashboard"]
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

mongo_client.close()
