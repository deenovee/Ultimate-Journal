from dataController.functions.mongo import MongoDB
from dataController.functions.display import Display
from bson import ObjectId

class Delete:
    def __init__(self, collection):
        self.db = MongoDB(collection)
        self.collection = collection
        self.display = Display(collection)

    def delete(self):
        try:
            existingData = list(self.db.get({}))
        except Exception as e:
            print("Error retrieving data from database")
        if existingData:
            try:
                while True:
                    id = input("Enter Object ID to delete or list of IDs separated by /: ")
                    try:
                        id = str(id)
                        break
                    except ValueError:
                        print(ValueError)
                query = {"_id": id}
                try:
                    self.db.delete(query)
                except pymongo.errors.PyMongoError as e:
                    print(f"Failed to delete document: {e}")
                except Exception as e:
                    print(f"An error occurred: {e}")
            except KeyboardInterrupt:
                print("")
                print("Exiting...")
                print("")
            self.display.display()
        else:
            print("No data to delete")
            print("Exiting...")