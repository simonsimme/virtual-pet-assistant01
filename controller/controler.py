
import sys
import os
import pygame
from model import task
import datetime
from controller.cameraController import Camera
import threading

class PetController:
    def __init__(self, pet_model):
        self.pet = pet_model
        
        self.cleaning_active = False
        self.clean_icon = pygame.image.load(os.path.join("model","icons", "pixel", "scrub_brush.png")).convert_alpha()
        self.clean_tick = 0;
        self.isInventoryOpen = False
    def update_button_positions(self, window_width, window_height):
        """Update button positions dynamically based on window dimensions."""
        self.buttons = {
            "keyboard": self.create_button(os.path.join("model", "icons", "toolbar", "keyboard.png"), (10, window_height - 60 )),
            "clean": self.create_button(os.path.join("model", "icons", "pixel", "scrub_brush.png"), (window_width - 60, window_height - 60 )),
            "explore": self.create_button(os.path.join("model", "icons", "Misc", "Map.png"), (window_width - 120, window_height - 60 )),
            "bag": self.create_button(os.path.join("model", "icons", "Equipment", "Bag.png"), (window_width - 180, window_height - 60 ))
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


        if self.cleaning_active:
            # Allow toggling cleaning mode off by clicking the clean button again
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.buttons["clean"][1].collidepoint(event.pos):
                print("here")
                self.cleaning_active = not self.cleaning_active
                self.pet.change_activity("idle")  
                pygame.mouse.set_visible(True)
            # If cleaning mode is active, check for drag over pet
            elif event.type == pygame.MOUSEMOTION and event.buttons[0] and self.pet.clean_cooldown < 100:
                # Use view's sprite size and scale for pet collision
                pet_x, pet_y = self.view.get_center_pos()
                pet_w = self.view.sprite_width * self.view.scale
                pet_h = self.view.sprite_height * self.view.scale
                pet_rect = pygame.Rect(pet_x, pet_y, pet_w, pet_h)
                
                if pet_rect.collidepoint(event.pos):
                    self.clean_tick += 1
                    if self.clean_tick > 20:  # Adjust threshold as needed
                        self.pet.clean_pet()
                        self.clean_tick = 0  # Reset tick after cleaning
            elif (self.cleaning_active and self.pet.clean_cooldown >= 100) or not self.pet.petIsAlive:
                self.cleaning_active = False
                self.pet.change_activity("idle")
                pygame.mouse.set_visible(True)
                
        else:
            if event.type == pygame.MOUSEBUTTONDOWN :
                
                
                if event.button == 1 and self.buttons["keyboard"][1].collidepoint(event.pos):
                    self.view.isChatopen = not self.view.isChatopen
                elif event.button == 1 and self.buttons["bag"][1].collidepoint(event.pos):
                    self.isInventoryOpen = not self.isInventoryOpen
                elif event.button == 1 and self.isInventoryOpen:
                    mouse_x, mouse_y = event.pos
                    for rect, entry in self.view.inventory_item_rects:
                        if rect.collidepoint(mouse_x, mouse_y):
                            entry["item"].use(self.pet)
                            break
                # Check if the clean button was clicked      
                elif event.button == 1 and self.buttons["clean"][1].collidepoint(event.pos):
                    if self.pet.clean_cooldown >= 100:
                        print('cooldown')
                    else:
                        self.pet.change_activity("clean")
                        self.cleaning_active = not self.cleaning_active
                    # Hide system cursor, draw icon at mouse in view.draw
                    pygame.mouse.set_visible(False)
                elif event.button == 1 and self.buttons["explore"][1].collidepoint(event.pos):
                    print("explore button clicked")
                    
                    if self.pet.current_activity == "explore":
                        self.pet.change_activity("idle")
                    else:
                        self.pet.change_activity("explore")
                        explore_thread = threading.Thread(target=self.pet.start_explore, daemon=True)
                        explore_thread.start()
            if event.type == pygame.MOUSEWHEEL and self.isInventoryOpen:
                self.view.inventory_scroll -= event.y
        if not self.pet.petIsAlive and self.cleaning_active:
            self.cleaning_active = False
            self.pet.change_activity("idle")
            pygame.mouse.set_visible(True)

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
