
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

        # --- Chat panel handle drag logic ---
        if self.view.isChatopen:
            # Handle dragging the chat panel handle to resize
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.view.chat_handle_rect and self.view.chat_handle_rect.collidepoint(event.pos):
                    self.view.dragging_chat_handle = True
                    self.view._drag_offset = event.pos[1] - self.view.chat_handle_rect.y
            elif event.type == pygame.MOUSEBUTTONUP:
                self.view.dragging_chat_handle = False
            elif event.type == pygame.MOUSEMOTION:
                if getattr(self.view, 'dragging_chat_handle', False):
                    new_height = self.view.window_height - (event.pos[1] + getattr(self.view, '_drag_offset', 0))
                    min_panel_height = 80
                    max_panel_height = self.view.window_height - 100
                    self.view.chat_panel_height = max(min_panel_height, min(new_height, max_panel_height))

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.buttons["feed"][1].collidepoint(event.pos):
                self.pet.feed(5)
            elif event.button == 1 and self.buttons["keyboard"][1].collidepoint(event.pos):
                self.view.isChatopen = not self.view.isChatopen
                #print("Chat panel toggled:", self.view.isChatopen)

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
