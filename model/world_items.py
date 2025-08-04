from model.item import Food  # Make sure this import path is correct
import sys
import os
class world_items:
    
    def __init__(self):
        
        self.food_items = {
            "Fish": Food("Fish", 20, 10, self.get_resource_path("model/icons/Food/Fish Steak.png")),
            "Steak": Food("Steak", 30, 15, self.get_resource_path("model/icons/Food/Meat.png")),
        }
    @staticmethod
    def get_resource_path(relative_path):
        """Get the absolute path to a resource, works for dev and PyInstaller."""
        if getattr(sys, 'frozen', False):  # Check if running as a PyInstaller bundle
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)


    