from model.world_items import world_items
from . import task
import random
import time
import pygame
import os
from . import save_load

class virtual_pet:
    def __init__(self, name, cat_nr=5, game_view=None, god_mode=False):
        self.name = name
        self.hunger = random.randint(30,60) # 0 starving, 100 full
        self.mood = "Happy"
        self.moodSlider = random.randint(60,80) # 0 sad, 100 happy
        self.energy = random.randint(30,70) # 0 exhausted, 100 energized
        self.age = 0
        self.health = random.randint(60, 100)  # 0 dead, 100 healthy
        self.clean = random.randint(3, 40)  # 0 dirty, 100 clean
        self.clean_cooldown = 0
        self.tasks = []
        self.birth_date = time.strftime("%Y-%m-%d")
        self.inventory = [] # List of dicts: {"item": item_object, "quantity": int}
        
        self.animations = {}
        self.current_animation = "NONE"
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_delay = 75  # ms per frame

        self.activities = ["explore", "sleep", "eat", "clean", "idle","low-stats"]
        self.current_activity = "idle"

        self.stop_states = ["laying", "sit"]
        
        self.moving_states = ["walk", "stretch", "run"]

        self.active_states = ["walk", "stretch", "run","lick", "itch"]
        self.petIsAlive = True

        frame_size = (50,50)
        self.view = game_view
        self.cat_nr = cat_nr
        self.god_mode = god_mode
        
       # Load all animations using cat_nr
        self.load_animation("walk", f"model/assets/Pet Cats Pack/Cat-{cat_nr}/Cat-{cat_nr}-Walk.png", frame_size , 8)
        self.load_animation("stretch", f"model/assets/Pet Cats Pack/Cat-{cat_nr}/Cat-{cat_nr}-Stretching.png", frame_size , 13)
        self.load_animation("run", f"model/assets/Pet Cats Pack/Cat-{cat_nr}/Cat-{cat_nr}-Run.png", frame_size , 8)
        self.load_animation("sleep1", f"model/assets/Pet Cats Pack/Cat-{cat_nr}/Cat-{cat_nr}-Sleeping1.png", frame_size , 1)
        self.load_animation("sleep2", f"model/assets/Pet Cats Pack/Cat-{cat_nr}/Cat-{cat_nr}-Sleeping2.png", frame_size , 1)
        self.load_animation("sit", f"model/assets/Pet Cats Pack/Cat-{cat_nr}/Cat-{cat_nr}-Sitting.png", frame_size , 1)
        self.load_animation("meow", f"model/assets/Pet Cats Pack/Cat-{cat_nr}/Cat-{cat_nr}-Meow.png", frame_size , 4)
        self.load_animation("lick", f"model/assets/Pet Cats Pack/Cat-{cat_nr}/Cat-{cat_nr}-Licking 1.png", frame_size , 5)
        self.load_animation("lick2", f"model/assets/Pet Cats Pack/Cat-{cat_nr}/Cat-{cat_nr}-Licking 2.png", frame_size , 5)
        self.load_animation("itch", f"model/assets/Pet Cats Pack/Cat-{cat_nr}/Cat-{cat_nr}-Itch.png", frame_size , 2)
        self.load_animation("laying", f"model/assets/Pet Cats Pack/Cat-{cat_nr}/Cat-{cat_nr}-Laying.png", frame_size , 8)
        
    def set_game_view(self, game_view):
        """Set the game view for the pet."""
        self.view = game_view
      

    def set_screen(self,screen, pos, scale=2):
        self.screen = screen
        self.screen_pos = pos
        self.scale = scale
    
    def load_animation(self, name, sprite_sheet_path, frame_size, num_frames):
        sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        frames = []
        frame_width, frame_height = frame_size
        for i in range(num_frames):
            frame_surface = pygame.Surface(frame_size, pygame.SRCALPHA)
            frame_surface.blit(
                sprite_sheet,
                (0, 0),
                pygame.Rect(i * frame_width, 0, frame_width, frame_height)
            )
            frames.append(frame_surface)
        self.animations[name] = frames
        
    def play_animation(self, screen, pos, dt, name=None, scale=2):
        stop_at_last = False
        if name in self.stop_states or name is None:
            stop_at_last = True
        if name is not None:
            if name in self.animations:
                if self.current_animation != name:
                    self.current_animation = name
                    self.current_frame = 0  # Reset frame on animation switch
            else:
                print("error animation name:" + str(name))
        frames = self.animations.get(self.current_animation, [])
        if not frames:
            return
        self.frame_timer += dt
        if self.frame_timer >= self.frame_delay:
            if stop_at_last:
                if self.current_frame < len(frames) - 1:
                    self.current_frame += 1
                # else: stay at last frame
            else:
                self.current_frame = (self.current_frame + 1) % len(frames)
            self.frame_timer = 0
        # print(name)
        if self.current_frame >= len(frames):
            self.current_frame = 0
# ... rest of your code ...
        frame = frames[self.current_frame]
        frame = pygame.transform.scale(frame, (frame.get_width() * scale, frame.get_height() * scale))
        screen.blit(frame, pos)
        #print("playing",name)
        
    def feed(self, food):
        if self.hunger >= 100:
            print(f"{self.name} is not hungry.")
            return
        self.hunger += food
        if self.hunger > 100:
            self.hunger = 100
        if self.moodSlider < 45:
            self.moodSlider += 20
            self.energy += 10
        else:
            self.moodSlider += 10
            self.energy += 5
        if self.moodSlider > 100:
            self.moodSlider = 100
    
    def change_activity(self, activity):
        
        if activity not in self.activities:
            print(f"Invalid activity: {activity}")
            return
        
        if self.current_activity == "low-stats":
            self.view.add_event_text(f"{self.name} is too tired or hungry to do anything else.")
            return
        if self.current_activity == activity:
            return
        
        if activity == "explore":
            if self.energy < 20 or self.hunger < 20:
                self.view.add_event_text(f"{self.name} is too tired or hungry to explore.")
                return
            self.current_animation = random.choice(self.moving_states)
        if activity == "clean":
            if self.clean >= 100:
                self.view.add_event_text(f"{self.name} is already clean.")
                #print(f"{self.name} is already clean.")
                return
            self.current_animation = "sit"
        self.current_activity = activity
        
    def clean_pet(self):
        if self.clean >= 100 or not self.petIsAlive or self.clean_cooldown >= 100:
            #print(f"{self.name} is already clean.")
            return
        base = 4  # max amount added when very dirty
        # The closer to 100, the smaller the increment
        increment = base * (1 - (self.clean / 100))  # e.g., at 90, only 0.5 is added
        if increment < 0.1:
            increment = 0.05  # minimum increment
        self.clean += increment
        if self.clean >= 100:
            self.clean = 100
        self.clean_cooldown += 5
        
    def pet_died(self):
        print(f"{self.name} has died.")
        animation_switch = "laying"  # Dead or very sick
        self.petIsAlive = False
        self.current_animation = animation_switch 
        
        
        
        
    def update_animation(self):
        # Animation logic based on pet's parameters
        
        animation_switch = ""
        
        self.clean_cooldown = max(0, self.clean_cooldown - random.randint(5, 10))  # Decrease cooldown over time

        if self.health <= 0:
           
            self.pet_died()
            return
            
        elif self.energy < 20 and self.current_animation == "laying":
            if self.hunger < 30:
                animation_switch = "sleep2"  # Very tired and hungry
            else:
                animation_switch = "sleep1"  # Just tired
        elif self.hunger < 30:
            animation_switch = "meow"  # Hungry and asking for food
        elif self.moodSlider < 25:
            animation_switch = "itch"  # Sad or uncomfortable
        elif self.energy > 80 and self.moodSlider > 70:
            animation_switch = "run"  # Very happy and energetic
        elif self.current_activity == "explore":
            animation_switch = random.choice(self.moving_states)  # Random active state
            self.moodSlider += random.randint(4, 8)
            self.energy -= random.randint(1, 3)  
            self.hunger -= random.randint(1, 3)
            self.clean -= random.randint(1, 3)  
            self.current_animation = animation_switch
        elif self.current_activity == "clean":
            self.current_animation = "sit"  # Cleaning state
        
        else:
            animation_switch = random.choice(self.stop_states + self.active_states)

        if self.current_animation != animation_switch and self.current_activity == "idle":
            animation_switch = random.choice(self.stop_states + self.active_states)
            self.current_animation = animation_switch
        self.cap_stats()
        if self.god_mode:
            self.hunger = 100
            self.moodSlider = 100
            self.energy = 100
            self.clean = 100
            self.health = 100
        
        
    def update_pet(self):
        self.age += 1  # 1 per 10 min
        
        if self.god_mode:
            self.hunger = 100
            self.moodSlider = 100
            self.energy = 100
            self.clean = 100
            self.health = 100
            return
        # Age: 1 week in real time = 1 year for the pet
        if self.health <= 0:
           
            self.pet_died()
            return
        

        if self.hunger > 0:
            self.hunger -= random.randint(1, 5)
        if self.moodSlider > 0 and (self.hunger < 30 or self.energy < 20):
            self.moodSlider -= random.randint(1, 5 )
            if self.moodSlider < 0:
                self.moodSlider = 0

        if self.energy > 0 and self.hunger < 30:
            self.energy -= random.randint(1, 5)
        if self.hunger < 30:
            self.mood = "Hungry"
        elif self.moodSlider < 25:
            self.mood = "Sad"
        elif self.energy < 20:
            self.mood = "Tired"
        elif self.clean < 15:
            self.mood = "Dirty"
        else:
            self.mood = "Happy"

        age_multiplier = 0
        if self.age > 50:
            age_multiplier = 2
        elif self.age > 100:
            age_multiplier = 5

        if self.hunger < 15:
            self.health += self.hunger - 15 - age_multiplier
        if self.energy < 15:
            self.health += self.energy - 15 - age_multiplier
        if self.clean < 10:
            self.health += self.clean - 10 - age_multiplier
            
        self.cap_stats()


    def cap_stats(self):
        self.hunger = max(0, min(self.hunger, 100))
        self.moodSlider = max(0, min(self.moodSlider, 100))
        self.energy = max(0, min(self.energy, 100))
        self.clean = max(0, min(self.clean, 100))
        self.health = max(0, min(self.health, 100))
        
    def start_explore(self):
        """Start the explore activity."""
        if self.energy < 10 or self.hunger < 10:
            print(f"{self.name} is too tired or hungry to explore.")
            return
        item_chance = 50 #percent chance to find an item
        while self.current_activity == "explore":
            if random.randint(1, 100) <= item_chance:
                found_item = random.choice(list(world_items().food_items.values()))
                self.add_item_inventory(found_item)
                self.view.add_event_text(f"{self.name} found a {found_item.name}!")
                #print(f"{self.name} found a {found_item.name}!")
            time.sleep(3)

    def add_item_inventory(self, item, quantity=1):
        """Add an item and quantity to the pet's inventory."""
        # Check if item already exists in inventory
        for entry in self.inventory:
            if entry["item"].name == item.name:
                entry["quantity"] += quantity
                return
        # If not found, add new entry
        self.inventory.append({"item": item, "quantity": quantity})

    def remove_item_inventory(self, item, quantity=1):
        """Remove a quantity of an item from the inventory. Removes entry if quantity reaches 0."""
        for entry in self.inventory:
            if entry["item"].name == item.name:
                entry["quantity"] -= quantity
                if entry["quantity"] <= 0:
                    self.inventory.remove(entry)
                return
    def to_dict(self):
        return {
            "name": self.name,
            "mood": self.mood,
            "hunger": self.hunger,
            "energy": self.energy,
            "health": self.health,
            "clean": self.clean,
            "inventory": [
                {"item": item["item"].name, "quantity": item["quantity"]}
                for item in self.inventory
            ],
            "cat_nr": self.cat_nr,
            "age": self.age,
            "clean_cooldown": self.clean_cooldown  # Save clean cooldown
        }

    def from_dict(self, data, item_lookup):
        self.name = data["name"]
        self.mood = data["mood"]
        self.hunger = data["hunger"]
        self.energy = data["energy"]
        self.health = data["health"]
        self.clean = data["clean"]
        self.inventory = [
            {"item": item_lookup[item["item"]], "quantity": item["quantity"]}
            for item in data["inventory"]
        ]
        self.cat_nr = data.get("cat_nr", 5)
        self.age = data.get("age", 0)
        self.clean_cooldown = data.get("clean_cooldown", 0)
        
        
        
        
        
