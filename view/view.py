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
        self.inventory_scroll = 0
        self.inventory_item_rects = []
        self.event_text = []
    
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
        card_rect = (20, 20, self.window_width-40, 150)
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
        age_surf = stat_font.render(f"Age: {self.pet.age} weeks", True, (180, 150, 100))


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

        # Third row: clean and age
        row3_surfs = [clean_surf, age_surf]
        row3_width = sum(surf.get_width() for surf in row3_surfs) + 24 * (len(row3_surfs) - 1)
        row3_x = (self.window_width - row3_width) // 2
        row3_y = 135
        for i, surf in enumerate(row3_surfs):
            screen.blit(surf, (row3_x + i * (surf.get_width() + 24), row3_y))
        

        # Draw button with modern look
        for button_name, (button_img, button_rect) in self.controller.buttons.items():
            # Draw button background
            btn_rect = button_rect.inflate(12, 12)
            self.draw_rounded_rect(screen, (146, 179, 240), btn_rect, radius=14, shadow=True)
            screen.blit(button_img, button_rect)
            # Show cleaning cooldown over the clean button
            if button_name == "clean" and hasattr(self.pet, "clean_cooldown") and self.pet.clean_cooldown > 0:
                font = pygame.font.SysFont('Segoe UI', 16, bold=True)
                cooldown_text = font.render(f"{int(self.pet.clean_cooldown)}", True, (255, 50, 50))
                text_rect = cooldown_text.get_rect(center=(button_rect.centerx, button_rect.top - 12))
                screen.blit(cooldown_text, text_rect)
            
        #btn_rect = self.controller.button_rect.inflate(12, 12)
       # self.draw_rounded_rect(screen, (146, 179, 240), btn_rect, radius=14, shadow=True)
       #screen.blit(self.controller.button_img, self.controller.button_rect)

        # Draw pet sprite (centered)
        self.pet.set_screen(screen, self.get_center_pos(), self.scale)
        self.pet.play_animation(screen, self.get_center_pos(), dt, name=self.pet.current_animation, scale=self.scale)
        
        if self.event_text:
                event_font = pygame.font.SysFont('Segoe UI', 20, bold=True)
                center_x, center_y = self.get_center_pos()
                displayed_height = self.sprite_height * self.scale
                base_y = center_y + displayed_height + 10  # 10px below pet
                for i, msg in enumerate(self.event_text):
                    msg_surf = event_font.render(msg, True, (180, 220, 255))
                    msg_rect = msg_surf.get_rect(center=(self.window_width // 2, base_y + i * 28))
                    screen.blit(msg_surf, msg_rect)

        # Footer or helper text
        help_surf = label_font.render(self.pet.current_activity + "...", True, (120, 130, 160))
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
            
            
        
        if self.controller.isInventoryOpen:
            # Backpack panel settings
            inv_panel_width = 220
            inv_panel_height = min(self.window_height - 60, 340)
            inv_panel_x = self.window_width - inv_panel_width - 20
            inv_panel_y = self.window_height/2 - inv_panel_height/2
            inv_panel_rect = pygame.Rect(inv_panel_x, inv_panel_y, inv_panel_width, inv_panel_height)
            # Backpack look: brownish, rounded, with a "zipper" at the top
            self.draw_rounded_rect(screen, (181, 140, 90), inv_panel_rect, radius=32, shadow=True)
            zipper_rect = pygame.Rect(inv_panel_x + 30, inv_panel_y - 10, inv_panel_width - 60, 16)
            pygame.draw.rect(screen, (220, 200, 160), zipper_rect, border_radius=8)
            pygame.draw.rect(screen, (120, 90, 60), zipper_rect, 2, border_radius=8)

            # Inventory grid settings
            cols = 3
            padding = 10
            icon_size = 40
            start_x = inv_panel_x + 18
            start_y = inv_panel_y + 32
            font = pygame.font.SysFont('Segoe UI', 14)
            mouse_x, mouse_y = pygame.mouse.get_pos()
            hovered_entry = None

            # Scroll logic
            items_per_row = cols
            rows_visible = (inv_panel_height - 48) // (icon_size + 28)
            total_rows = (len(self.pet.inventory) + cols - 1) // cols
            max_scroll = max(0, total_rows - rows_visible)
            scroll = getattr(self, "inventory_scroll", 0)
            scroll = max(0, min(scroll, max_scroll))
            self.inventory_scroll = scroll

            # Only show visible items
            first_visible_idx = scroll * cols
            last_visible_idx = min(len(self.pet.inventory), first_visible_idx + rows_visible * cols)

            for idx in range(first_visible_idx, last_visible_idx):
                entry = self.pet.inventory[idx]
                item = entry["item"]
                quantity = entry["quantity"]
                rel_idx = idx - first_visible_idx
                row = rel_idx // cols
                col = rel_idx % cols
                x = start_x + col * (icon_size + padding)
                y = start_y + row * (icon_size + 28)
                item_rect = pygame.Rect(x, y, icon_size, icon_size)
                self.inventory_item_rects.append((item_rect, entry))

                # Draw icon background
                pygame.draw.rect(screen, (255, 245, 220), item_rect, border_radius=10)
                # Hover effect
                if item_rect.collidepoint(mouse_x, mouse_y):
                    pygame.draw.rect(screen, (180, 220, 255), item_rect, 3, border_radius=10)
                    hovered_entry = entry
                else:
                    pygame.draw.rect(screen, (181, 140, 90), item_rect, 2, border_radius=10)

                # Draw item icon if available
                if hasattr(item, "icon") and item.icon:
                    icon_img = pygame.transform.smoothscale(item.icon, (icon_size-8, icon_size-8))
                    screen.blit(icon_img, (x+4, y+4))
                else:
                    # Fallback: draw first letter
                    letter_surf = font.render(item.name[0], True, (120, 120, 180))
                    letter_rect = letter_surf.get_rect(center=item_rect.center)
                    screen.blit(letter_surf, letter_rect)

                # Draw quantity
                qty_surf = font.render(f"x{quantity}", True, (80, 80, 80))
                qty_rect = qty_surf.get_rect(bottomright=(x+icon_size-4, y+icon_size-4))
                screen.blit(qty_surf, qty_rect)

            # Draw item name below icon (only for hovered)
            if hovered_entry:
                item = hovered_entry["item"]
                tooltip_font = pygame.font.SysFont('Segoe UI', 16, bold=True)
                tooltip_text = getattr(item, "description", item.description if hasattr(item, "description") else item.name)
                tooltip_surf = tooltip_font.render(tooltip_text, True, (30, 30, 60))
                tooltip_bg = pygame.Surface((tooltip_surf.get_width()+16, tooltip_surf.get_height()+10), pygame.SRCALPHA)
                tooltip_bg.fill((255, 255, 255, 230))
                pygame.draw.rect(tooltip_bg, (181, 140, 90), tooltip_bg.get_rect(), 2, border_radius=8)
                tooltip_pos = (mouse_x + 12, mouse_y - 8)
                screen.blit(tooltip_bg, tooltip_pos)
                screen.blit(tooltip_surf, (tooltip_pos[0]+8, tooltip_pos[1]+5))

            # Draw scroll indicators if needed
            if max_scroll > 0:
                arrow_color = (120, 90, 60)
                arrow_up = [(inv_panel_x + inv_panel_width//2 - 10, inv_panel_y + 8),
                            (inv_panel_x + inv_panel_width//2 + 10, inv_panel_y + 8),
                            (inv_panel_x + inv_panel_width//2, inv_panel_y - 4)]
                arrow_down = [(inv_panel_x + inv_panel_width//2 - 10, inv_panel_y + inv_panel_height - 16),
                              (inv_panel_x + inv_panel_width//2 + 10, inv_panel_y + inv_panel_height - 16),
                              (inv_panel_x + inv_panel_width//2, inv_panel_y + inv_panel_height - 4)]
                if scroll > 0:
                    pygame.draw.polygon(screen, arrow_color, arrow_up)
                if scroll < max_scroll:
                    pygame.draw.polygon(screen, arrow_color, arrow_down)
                


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
    def add_event_text(self, text):
        """Add a new event message (max 3 shown)."""
        self.event_text.append(text)
        if len(self.event_text) > 3:
            self.event_text = self.event_text[-3:]
        print(text)


    def quit(self):
        pygame.quit()
        exit()