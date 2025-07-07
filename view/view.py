from model import pet
import pygame
import os
import cv2

class view:
    def __init__(self, pet, controller, window_width=300, window_height=300):
        self.pet = pet
        self.controller = controller
        self.window_width, self.window_height = window_width, window_height
        self.sprite_width, self.sprite_height = 50, 50  # Use your frame size here
        self.scale = 8
        self.isChatopen = False
        self.chat_input = ""
        self.chat_log = []
        self.chat_panel_height = self.window_height // 3
        self.dragging_chat_handle = False
        self.chat_handle_rect = None
    
    def window_resize(self, new_width, new_height):
        """Resize the window and update the view."""
        self.window_width = new_width
        self.window_height = new_height
        
    def get_center_pos(self):
        displayed_width = self.sprite_width * self.scale
        displayed_height = self.sprite_height * self.scale
        center_x = (self.window_width - displayed_width) // 2
        center_y = (self.window_height - displayed_height) // 2
        return center_x, center_y
        

    def draw_rounded_rect(self, surface, color, rect, radius=15, shadow=False):
        """Draw a rounded rectangle with optional shadow."""
        if shadow:
            shadow_color = (0, 0, 0, 60)
            shadow_surf = pygame.Surface((rect[2]+8, rect[3]+8), pygame.SRCALPHA)
            pygame.draw.rect(shadow_surf, shadow_color, (4, 4, rect[2], rect[3]), border_radius=radius+4)
            surface.blit(shadow_surf, (rect[0]-4, rect[1]-4))
        pygame.draw.rect(surface, color, rect, border_radius=radius)

    def draw(self, screen, dt):
        # Soft background color
        screen.fill((240, 245, 255))

        # Card for pet stats
        card_rect = (20, 20, self.window_width-40, 110)
        self.draw_rounded_rect(screen, (255, 255, 255), card_rect, radius=18, shadow=True)

        # Modern font
        name_font = pygame.font.SysFont('Segoe UI', 32, bold=True)
        stat_font = pygame.font.SysFont('Segoe UI', 22)
        label_font = pygame.font.SysFont('Segoe UI', 18, italic=True)


        # Pet name (centered in card)
        name_surf = name_font.render(self.pet.name, True, (40, 60, 120))
        name_rect = name_surf.get_rect(center=(self.window_width//2, 40))
        screen.blit(name_surf, name_rect)

        # Stats with color accents
        mood_surf = stat_font.render(f"Mood: {self.pet.mood}", True, (120, 120, 255))
        hunger_surf = stat_font.render(f"Hunger: {self.pet.hunger}", True, (255, 180, 80))
        energy_surf = stat_font.render(f"Energy: {self.pet.energy}", True, (80, 200, 255))
        health_surf = stat_font.render(f"Health: {self.pet.health}", True, (80, 220, 120))
        clean_surf = stat_font.render(f"Clean: {int(self.pet.clean)}", True, (200, 200, 200))


        # Center stats in the card
        # First row: mood and hunger
        row1_surfs = [mood_surf, hunger_surf]
        row1_width = mood_surf.get_width() + 24 + hunger_surf.get_width()
        row1_x = (self.window_width - row1_width) // 2
        row1_y = 75
        screen.blit(mood_surf, (row1_x, row1_y))
        screen.blit(hunger_surf, (row1_x + mood_surf.get_width() + 24, row1_y))

        # Second row: energy and health
        row2_surfs = [energy_surf, health_surf]
        row2_width = energy_surf.get_width() + 24 + health_surf.get_width()
        row2_x = (self.window_width - row2_width) // 2
        row2_y = 105
        screen.blit(energy_surf, (row2_x, row2_y))
        screen.blit(health_surf, (row2_x + energy_surf.get_width() + 24, row2_y))

        # Third row: clean
        row3_surfs = [clean_surf]
        row3_width = clean_surf.get_width()
        row3_x = (self.window_width - row3_width) // 2
        row3_y = 135
        screen.blit(clean_surf, (row3_x, row3_y))

        # Draw button with modern look
        for button_name, (button_img, button_rect) in self.controller.buttons.items():
            # Draw button background
            btn_rect = button_rect.inflate(12, 12)
            self.draw_rounded_rect(screen, (146, 179, 240), btn_rect, radius=14, shadow=True)
            screen.blit(button_img, button_rect)
            
        #btn_rect = self.controller.button_rect.inflate(12, 12)
       # self.draw_rounded_rect(screen, (146, 179, 240), btn_rect, radius=14, shadow=True)
       #screen.blit(self.controller.button_img, self.controller.button_rect)

        # Draw pet sprite (centered)
        self.pet.set_screen(screen, self.get_center_pos(), self.scale)
        self.pet.play_animation(screen, self.get_center_pos(), dt, name=self.pet.current_animation, scale=self.scale)

        # Footer or helper text
        help_surf = label_font.render("Say 'Hey Adam' to interact!", True, (120, 130, 160))
        help_rect = help_surf.get_rect(center=(self.window_width//2, self.window_height-18))
        screen.blit(help_surf, help_rect)
        
        if self.isChatopen:
            # Use self.chat_panel_height for resizable panel
            min_panel_height = 80
            max_panel_height = self.window_height - 100
            self.chat_panel_height = max(min_panel_height, min(self.chat_panel_height, max_panel_height))
            panel_height = self.chat_panel_height
            panel_rect = pygame.Rect(0, self.window_height - panel_height, self.window_width, panel_height)
            pygame.draw.rect(screen, (230, 230, 250), panel_rect)
            pygame.draw.rect(screen, (180, 180, 220), panel_rect, 2)

            # Draw draggable handle
            handle_height = 8
            handle_rect = pygame.Rect(0, self.window_height - panel_height - handle_height, self.window_width, handle_height)
            pygame.draw.rect(screen, (180, 180, 220), handle_rect)
            self.chat_handle_rect = handle_rect

            # Draw chat log (last 5 messages)
            font = pygame.font.SysFont('Segoe UI', 18)
            y = self.window_height - panel_height + 10
            for sender, msg in self.chat_log[-5:]:
                msg_surf = font.render(f"{sender}: {msg}", True, (50, 50, 80))
                screen.blit(msg_surf, (10, y))
                y += 22

            # Draw input field
            input_rect = pygame.Rect(10, self.window_height - 40, self.window_width - 20, 30)
            pygame.draw.rect(screen, (255, 255, 255), input_rect)
            pygame.draw.rect(screen, (180, 180, 220), input_rect, 2)
            input_surf = font.render(self.chat_input, True, (0, 0, 0))
            screen.blit(input_surf, (input_rect.x + 5, input_rect.y + 5))
            
        


        # Draw custom cleaning cursor if cleaning is active
        if getattr(self.controller, 'cleaning_active', False):
            mouse_x, mouse_y = pygame.mouse.get_pos()
            icon = self.controller.buttons["clean"][0]
            icon_rect = icon.get_rect(center=(mouse_x, mouse_y))
            screen.blit(icon, icon_rect)

        pygame.display.flip()
    def pet_chat_response(self, response):
        """Add a response from the pet to the chat log."""
        self.chat_log.append((self.pet.name, response))
        

    def show_frame(self, frame):
        """Display the given frame on the screen."""
        cv2.imshow("Selfie", frame)
        
        cv2.waitKey(0)


    def quit(self):
        pygame.quit()
        exit()