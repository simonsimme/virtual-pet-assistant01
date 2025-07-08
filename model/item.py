import pygame




class Item:
    """Base class for items in the virtual pet game."""
    def __init__(self, name, icon_path=None):
        self.name = name
        self.icon = None  # Placeholder for item icon
        if icon_path:
            self.load_icon(icon_path)

    def load_icon(self, path):
        """Load the icon image from the specified path."""
        self.icon = pygame.image.load(path).convert_alpha()

    def use(self, pet, removable=True):
        """Use the item on the pet. This method should be overridden by subclasses."""
        raise NotImplementedError("Subclasses must implement this method.")

class Food(Item):
    def __init__(self, name, hunger_recovery, mood_recovery=0, icon_path=None):
        super().__init__(name, icon_path)
        self.hunger_recovery = hunger_recovery
        self.mood_recovery = mood_recovery
        self.description = f"{name} - Restores {hunger_recovery} hunger and {mood_recovery} mood."

    def load_icon(self, path):
        self.icon = pygame.image.load(path).convert_alpha()
        
    def use(self, pet, removable=True):
        """Consume the food item and apply its effects to the pet."""
        if pet.hunger >= 100:
            #print(f"{pet.name} is already full!")
            return
        pet.hunger = min(pet.hunger + self.hunger_recovery, 100)
        pet.moodSlider = min(pet.moodSlider + self.mood_recovery, 100)
        if removable:
            pet.remove_item_inventory(self)