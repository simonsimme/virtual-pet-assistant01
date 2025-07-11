
import sys
import os
from matplotlib import scale
import pygame
import threading
from . import pet
from controller import PetController, Camera
from view import view
from . import googledochelper
import random
from . import save_load
from . import world_items


 

def main():
    pygame.init()
    pygame.display.set_caption("Virtual Pet Assistant")
    pygame.display.set_icon(pygame.image.load(
        os.path.join("model","idle animation", "sprite0.png")))
    
    windowwidth, windowheight = 400, 400
    screen = pygame.display.set_mode((windowwidth, windowheight), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    
    prev_game = save_load.save_exists()  # Check if a save file exists
    if prev_game:
        my_pet = pet.virtual_pet("adam")
        has_previous_game = save_load.load_game(my_pet, world_items.world_items().food_items)
    else:
        cat_options = [
    {"id": 1, "display": "Pissy orange"},
    {"id": 2, "display": "Batman"},
    {"id": 3, "display": "Sigma white"},
    {"id": 4, "display": "Weird brown"},
    {"id": 5, "display": "whity"},
    {"id": 6, "display": "Grey catty"},
]
        cat_nr, pet_name = start_screen(screen, cat_options)
        my_pet = pet.virtual_pet(pet_name, cat_nr=cat_nr)

    pet_thread = threading.Thread(target=my_pet.update_pet, args=(screen,), daemon=True)
    controller = PetController(my_pet)
    
    game_view = view(my_pet, controller, window_width=windowwidth, window_height=windowheight)
    controller.setView(game_view)
    view_thread = threading.Thread(target=game_view.draw, args=(screen, 0), daemon=True)
    view_thread.start()
    
    my_pet.set_game_view(game_view)
    
    
    
   
        

    # Import SpeechAssistant here to avoid circular import
    from . import speech_rec
    speech_assistant = speech_rec.SpeechAssistant(screen, game_view, my_pet.name, wake_word="hey adam")
    speech_thread = threading.Thread(target=speech_assistant.run, daemon=True)
    speech_thread.start()

    update_interval = 600000  # 10 minutes in milliseconds
    update_timer = 0
    
    update_activity_interval = 15000  # 15 seconds in milliseconds
    update_activity_timer = 70000

    running = True
    first = True
    while running:
        dt = clock.tick(60)  # milliseconds since last frame
        update_timer += dt
        update_activity_timer += dt
        game_view.draw(screen, dt)
        if first:
            pet_thread.start()
            first = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                save_load.save_game(my_pet)
            elif event.type == pygame.VIDEORESIZE:
                windowwidth, windowheight = event.w, event.h
                screen = pygame.display.set_mode((windowwidth, windowheight), pygame.RESIZABLE)
                game_view.window_resize(windowwidth, windowheight)
            if game_view.isChatopen and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if game_view.chat_input.strip():
                        game_view.chat_log.append(("You", game_view.chat_input))
                        prev_log = ""
                        if len(game_view.chat_log) > 1:
                            prev_sender, prev_msg = game_view.chat_log[-2]
                            prev_log = f"{prev_sender}: {prev_msg}"

                        def chat_llm_thread():
                            speech_assistant.handle_response_text(
                                f"PREVIOUS CONVERSATION [{prev_log}] NEW USER COMMAND [{game_view.chat_input}]"
                            )

                        threading.Thread(target=chat_llm_thread, daemon=True).start()
                        game_view.chat_input = ""
                elif event.key == pygame.K_BACKSPACE:
                    game_view.chat_input = game_view.chat_input[:-1]
                elif event.unicode and event.unicode.isprintable():
                    game_view.chat_input += event.unicode
            else:
                controller.handle_event(event)
            #my_pet.play_idle(screen, (game_view.center_x, game_view.center_y), dt)
        if update_timer >= update_interval:
            my_pet.update_pet()
            update_timer = 0
        if update_activity_timer >= update_activity_interval:
            my_pet.update_animation()
            update_activity_timer = 0
            update_activity_interval = random.randint(3000, 45000)  # Random interval between 3 and 45 seconds
        #if my_pet.idle_timer >= my_pet.idle_interval_threshold and my_pet.current_animation != "NONE":
            # In your main loop or view.draw:
           # my_pet.play_animation(screen, my_pet.screen_pos, dt, my_pet.current_animation, my_pet.scale, stop_at_last=True)
            #my_pet.idle_timer = 0
           # print("here")
        pygame.display.flip()
    speech_assistant.exit()
    pygame.quit()
    
    
def start_screen(screen, cat_options):
    font = pygame.font.SysFont('Segoe UI', 32, bold=True)
    small_font = pygame.font.SysFont('Segoe UI', 22)
    input_active = False
    name_input = ""
    selected_cat = len(cat_options) // 2

    # Load cat images (first frame of "sit" animation for each cat)
    cat_images = []
    for cat in cat_options:
        cat_nr = cat["id"]
        sprite_path = f"model/assets/Pet Cats Pack/Cat-{cat_nr}/Cat-{cat_nr}-Sitting.png"
        try:
            sprite_sheet = pygame.image.load(sprite_path).convert_alpha()
            cat_images.append(sprite_sheet)
        except Exception as e:
            cat_images.append(pygame.Surface((50, 50), pygame.SRCALPHA))

    clock = pygame.time.Clock()
    while True:
        screen.fill((230, 240, 255))
        width, height = screen.get_size()

        small_font_size = min(20, int(width * 0.025))  
        small_font_cat = pygame.font.SysFont('Segoe UI', small_font_size)

        # Dynamic scaling
        cat_area_width = width * 0.85
        cat_width = int(min(100, cat_area_width // len(cat_options) * 0.8))
        cat_height = cat_width
        cat_spacing = int((cat_area_width - (cat_width * len(cat_options))) // (len(cat_options) - 1)) if len(cat_options) > 1 else 0
        start_x = (width - (cat_width * len(cat_options) + cat_spacing * (len(cat_options) - 1))) // 2
        y = int(height * 0.22)

        # Title
        title = font.render("Choose your cat and name!", True, (60, 80, 120))
        screen.blit(title, (width // 2 - title.get_width() // 2, int(height * 0.07)))

        # Draw cat options as images
        for i, cat in enumerate(cat_options):
            x = start_x + i * (cat_width + cat_spacing)
            # Highlight selected cat
            border_color = (120, 180, 255) if i == selected_cat else (180, 180, 180)
            pygame.draw.rect(screen, border_color, (x-4, y-4, cat_width+8, cat_height+8), 4)
            # Scale cat image to fit
            scaled_img = pygame.transform.smoothscale(cat_images[i], (cat_width, cat_height))
            screen.blit(scaled_img, (x, y))
            # Draw cat name below image
            cat_text = small_font_cat.render(cat["display"], True, border_color)
            screen.blit(cat_text, (x + cat_width // 2 - cat_text.get_width() // 2, y + cat_height + 5))

        # Draw name input box
        input_box_width = int(width * 0.6)
        input_box_height = 40
        input_box_x = (width - input_box_width) // 2
        input_box_y = y + cat_height + 50
        input_box = pygame.Rect(input_box_x, input_box_y, input_box_width, input_box_height)
        pygame.draw.rect(screen, (255,255,255), input_box)
        pygame.draw.rect(screen, (120,180,255) if input_active else (180,180,180), input_box, 2)
        name_surf = small_font.render(name_input or "Enter name...", True, (60, 80, 120))
        screen.blit(name_surf, (input_box.x+8, input_box.y+8))

        # Draw start button
        start_btn_width = 120
        start_btn_height = 40
        start_btn_x = width // 2 - start_btn_width // 2
        start_btn_y = input_box_y + input_box_height + 30
        start_btn = pygame.Rect(start_btn_x, start_btn_y, start_btn_width, start_btn_height)
        pygame.draw.rect(screen, (120,180,255), start_btn)
        btn_text = small_font.render("Start!", True, (255,255,255))
        screen.blit(btn_text, (start_btn.x + (start_btn.width - btn_text.get_width()) // 2, start_btn.y + 8))

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
            elif event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        name_input = name_input[:-1]
                    elif event.unicode.isprintable():
                        name_input += event.unicode
                else:
                    if event.key == pygame.K_LEFT:
                        selected_cat = (selected_cat - 1) % len(cat_options)
                    elif event.key == pygame.K_RIGHT:
                        selected_cat = (selected_cat + 1) % len(cat_options)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    input_active = True
                else:
                    input_active = False
                # Check if a cat image was clicked
                for i, cat in enumerate(cat_options):
                    x = start_x + i * (cat_width + cat_spacing)
                    if pygame.Rect(x, y, cat_width, cat_height).collidepoint(event.pos):
                        selected_cat = i
                if start_btn.collidepoint(event.pos) and name_input.strip():
                    return cat_options[selected_cat]["id"], name_input.strip().lower()