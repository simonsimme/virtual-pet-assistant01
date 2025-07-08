from model.item import Food  # Make sure this import path is correct

class world_items:
    def __init__(self):
        
        self.food_items = {
            "Fish": Food("Fish", 20, 10, "model/icons/Food/Fish Steak.png"),
            "Steak": Food("Steak", 30, 15, "model/icons/Food/Meat.png"),
        }


    