from . import task
import random
import time
import pygame
import os

class virtual_pet:
    def __init__(self, name, cat_nr=5 ):
        self.name = name
        self.hunger = 50 # 0 starving, 100 full
        self.mood = "Happy"
        self.moodSlider = 80 # 0 sad, 100 happy
        self.energy = 50 # 0 exhausted, 100 energized
        self.age = 0
        self.health = 100
        self.tasks = []
        self.birth_date = time.strftime("%Y-%m-%d")
        self.last_fed = time.time()
        
        self.animations = {}
        self.current_animation = "NONE"
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_delay = 75  # ms per frame
       
        
        self.stop_states = ["laying", "sit"]

        self.active_states = ["walk", "stretch", "run","lick", "itch"]

        frame_size = (50,50)
        
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
        
   
    def update_animation(self):
        # Animation logic based on pet's parameters
        animation_switch = ""
        
        

        if self.health <= 0:
            animation_switch = "laying"  # Dead or very sick
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
        else:
            animation_switch = random.choice(self.stop_states + self.active_states)

        if self.current_animation != animation_switch:
            animation_switch = random.choice(self.stop_states + self.active_states)
            self.current_animation = animation_switch
        
    def update_pet(self):
        # Age: 1 week in real time = 1 year for the pet
        current_time = time.time()
        birth_time = time.mktime(time.strptime(self.birth_date, "%Y-%m-%d"))
        weeks_since_birth = int((current_time - birth_time) // (7 * 24 * 60 * 60))
        self.age = weeks_since_birth  # 1 week = 1 year

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
        else:
            self.mood = "Happy"

        age_multiplier = 0
        if self.age > 50:
            age_multiplier = 2

        if self.hunger < 15:
            self.health += self.hunger - 15 - age_multiplier
        if self.energy < 15:
            self.health += self.energy - 15 - age_multiplier

        self.health = max(self.health, 0)
        
        
        
