from nutrition import Nutrition
from exercise import Exercise
from sleep import Sleep


class Health:
    def __init__(self):
        self.sleep = Sleep()
        self.exercise = Exercise()
        self.nutrition = Nutrition()

    def sleep_dash(self):
        self.sleep.displayData()

    def exercise_dash(self):
        self.exercise.displayData()

    def nutrition_dash(self):
        self.nutrition.displayData()

    #Sleep functions
    def insert_sleep_doc(self):
        self.sleep.collectData()
    
    def delete_sleep_doc(self):
        self.sleep.deleteData()
    
    def update_sleep_doc(self):
        self.sleep.updateData()
    
    def filter_sleep_data(self):
        self.sleep.filterData()
    
    def display_all_sleep_data(self):
        self.sleep.displayAllData()

    #Exercise functions
    def insert_exercise_doc(self):
        self.exercise.collectData()

    def delete_exercise_doc(self):
        self.exercise.deleteData()

    def update_exercise_doc(self):
        self.exercise.updateData()
    
    def filter_exercise_data(self):
        self.exercise.filterData()
    
    def display_all_exercise_data(self):
        self.exercise.displayAllData()
    
    #Nutrition functions
    def insert_nutrition_doc(self):
        self.nutrition.collectData()

    def delete_nutrition_doc(self):
        self.nutrition.deleteData()

    def update_nutrition_doc(self):
        self.nutrition.updateData()
    
    def filter_nutrition_data(self):
        self.nutrition.filterData()

    def display_all_nutrition_data(self):
        self.nutrition.displayAllData()

    


        

    