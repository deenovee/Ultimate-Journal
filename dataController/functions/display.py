from dataController.functions.mongo import MongoDB
from bson import ObjectId
import datetime
from datetime import date, timedelta
import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet


class Display:
    def __init__(self, collection):
        load_dotenv()
        self.db = MongoDB(collection)
        self.collection = collection
        self.bank_1 = os.getenv("BANK_1")
        self.key = self.load_key()

    
    def load_key(self):
        key_path = os.getenv("KEY")
        if os.path.exists(key_path):
            with open(key_path, "rb") as key_file:
                key = key_file.read()
        return key

    def decrypt(self, encrypted_data):
        cipher_suite = Fernet(self.key)
        decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
        return decrypted_data

    def display(self):
        if self.collection == "journal":
            start_date = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
            query = {"date": {"$gte": start_date}}
        elif self.collection == "sleep":
            start_date = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=7)
            query = {"time_end": {"$gte": start_date}}
        elif self.collection == f"{self.bank_1}":
            start_date = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=7)
            query = {"transaction_date": {"$gte": start_date}}
        else:
            start_date = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=7)
            query = {"date": {"$gte": start_date}}

        try:
            records = list(self.db.get(query))
        except Exception as e:
            print("Error retrieving data from database")
            print(e)

        if records == []:
            print("No data to display")
        # elif self.collection == f"{self.bank_1}":
        #     keys = records[0].keys()
        #     for index, i in enumerate(records):
        #         j = index + 1
        #         output = f"Record {j}: \n"
        #         for key in keys:
        #             if key == "statement":
        #                 unencrypted = self.decrypt(i[key])
        #                 output += f"{key}: {unencrypted}"
        #             else:
        #                 output += f"{key}: {i[key]}\n"
        #         if j == len(records):
        #             print("")
        #             print(output)
        #             print("")
        #         else:
        #             print("")
        #             print(output)
        else:
            keys = records[0].keys()
            for index, i in enumerate(records):
                j = index + 1
                output = f"Record {j}: \n"
                for key in keys:
                    output += f"{key}: {i[key]}\n"
                if j == len(records):
                    print("")
                    print(output)
                    print("")
                else:
                    print("")
                    print(output)
                    