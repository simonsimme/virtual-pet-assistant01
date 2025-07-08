
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


 

def main():
    pygame.init()
    pygame.display.set_caption("Virtual Pet Assistant")
    pygame.display.set_icon(pygame.image.load(
        os.path.join("model","idle animation", "sprite0.png")))
    
    windowwidth, windowheight = 400, 400
    screen = pygame.display.set_mode((windowwidth, windowheight), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    my_pet = pet.virtual_pet("adam")
    pet_thread = threading.Thread(target=my_pet.update_pet, daemon=True)
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