
import sys
import os
import pygame
from model import task
import datetime
from controller.cameraController import Camera

class PetController:
    def __init__(self, pet_model):
        self.pet = pet_model
        self.buttons = {
            "feed": self.create_button(os.path.join("model","icons", "Monster Part", "Bone.png"), (10, 250)),
            "keyboard": self.create_button(os.path.join("model","icons", "toolbar", "keyboard.png"), (70, 250))
        }
    def setView(self, view):
        self.view = view

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return "quit"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.buttons["feed"][1].collidepoint(event.pos):
                self.pet.feed(5)
            elif event.button == 1 and self.buttons["keyboard"][1].collidepoint(event.pos):
                self.view.isChatopen = not self.view.isChatopen
        return None

    def add_schedule(self, string_task , start_time, duration_minutes):
        start_dt = datetime.datetime.fromisoformat(start_time)
        end_dt = start_dt + datetime.timedelta(minutes=duration_minutes)

        task.add_event(string_task, start_dt.isoformat(), end_dt.isoformat())
    
    def create_button(self, path_to_image, pos):
        button_img = pygame.image.load(path_to_image).convert_alpha()
        button_img = pygame.transform.smoothscale(button_img, (50, 50))
        button_rect = button_img.get_rect(topleft=pos)
        return button_img, button_rect
