import speech_recognition as sr
from .task import add_event
import datetime
import spacy
import dateparser
import pyttsx3
import os
from . import googledochelper
from . import googleToDo
from controller.cameraController import Camera
from view.view import view
from .ollama import LLM
import random
import playsound as ps
import sys
import re


class SpeechAssistant:
    def say(self, text):
        """Use text-to-speech to say the given text."""
        if self.game_view.isChatopen:
            self.game_view.pet_chat_response(text)
        else:
            self.engine.say(text)
            self.engine.runAndWait()
    def exit(self):
        self.llm.stop_ollama()
        self.stop_flag = True

    def __init__(self, screen, game_view, pet_name, wake_word, language="en-US"):
        self.wake_word = wake_word
        self.language = language
        self.recognizer = sr.Recognizer()
        try:
            self.mic = sr.Microphone()
        except Exception as e:
            print(f"Microphone initialization failed: {e}")
            self.mic = None
        self.engine = pyttsx3.init()
        self.screen = screen
        self.game_view = game_view
        self.llm = LLM(pet_name)
        self.name = pet_name
        self.stop_flag = False
        
    def listen_for_wake_word(self):
        if self.mic is None:
            print("Microphone not available. Please check your setup.")
            return False
        #print(f"Say '{self.wake_word}' to wake the assistant.")
        while True:
            if self.game_view.isChatopen:
                return False
            
            try:
                with self.mic as source:
                    self.recognizer.adjust_for_ambient_noise(source)
                    print("Listening...")
                    audio = self.recognizer.listen(source, phrase_time_limit=8)
                command = self.recognizer.recognize_google(audio, language=self.language).lower()
                print("You said:", command)
                greetings = [
                    "hello",
                    "Hi there!",
                    "Hey, I'm awake!",
                    "Ready when you are!",
                    "Hello, friend!",
                    "how can i help",
                    "How can I help you today?",
                    "IM ALIVE PLSS HELPPPP, eh ah, sorry, what can i help with today?"
                ]
                if self.wake_word in command or "wake up" in command:
                    self.say(random.choice(greetings))
                    print("Wake word detected!")
                    return True
            except sr.UnknownValueError:
                print("Sorry, I did not understand that.")
            except sr.RequestError:
                print("Could not contact Google Speech Recognition service.")
            except Exception as e:
                #print(f"Microphone error: {e}")
                return False

    def listen_for_command(self):
        if self.mic is None:
            print("Microphone not available. Please check your setup.")
            return ""
        print("Listening for your command...")
        try:
            with self.mic as source:
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source, phrase_time_limit=8)
            command = self.recognizer.recognize_google(audio, language=self.language).lower()
            print("Command:", command)
            return command
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
        except sr.RequestError:
            print("Could not contact Google Speech Recognition service.")
        except Exception as e:
            return ""
           #print(f"Microphone error: {e}")
        return ""

    

    def check_quick_commands(self, user_command):
        #quick commands: add event, take selfie. add todo, create document
        #format: 
        # !add event, title, date
        # !take selfie 
        # !add todo, title, notes, due date
        # !create document, title -:- content
        # !list tasks
        command = self.extract_user_command(user_command)
        if command is None or command[0] != "!":
            return False
        print("Quick command detected")
        command = command[1:]  # Remove the '!' prefix

        parts = command.split(",")
        response = ",".join(part.strip() for part in parts[1:])
        if parts[0] == "add event":
            self.handle_code(100, response)
        elif parts[0] == "take selfie":
            self.handle_code(106, "")
        elif parts[0] == "add todo":
            self.handle_code(103, response)
        elif parts[0] == "create document":
            self.handle_code(102, response)
        elif parts[0] == "list tasks":
            self.handle_code(104, "")
        else:
            self.say("Unknown command. Please try again.")
        return True
    def extract_user_command(self, input_string):
        """Extract the new user command from the input string."""
        match = re.search(r"NEW USER COMMAND \[(.*?)\]", input_string)
        if match:
            return match.group(1)  # Extract the content inside the brackets
        return None  # Return None if no match is found

    def handle_response_text(self, user_command):
        
            
        if self.check_quick_commands(user_command):
            return
        response = self.llm.ask_ollama( "TODAYS DAY AND TIME FOR THE USER: ["+ datetime.datetime.now().isoformat() + "]" + user_command)
        code = int(response[:5].replace("[", "").replace("]", ""))
        response = response[5:]
        print("LLM Response:", response)
        print(f"Code: {code}")
        self.handle_code(code, response)

    def handle_code(self, code, response):
        
                if code == 100:
                    # Extract event info from the full command
                    parts = response.split(",")
                    title = parts[0].strip() if len(parts) > 0 and parts[0].lower() != "empty" else None
                    start_str = parts[1].strip() if len(parts) > 1 and parts[1].lower() != "empty" else None
                    start = dateparser.parse(start_str) if start_str else None
                    print(f"Title: {title}, Start: {start}")

                    if title is None:
                        self.say("Could not extract event title. Please try again.")
                        return

                    if start is None:
                        self.say("Could not understand the date/time.")
                        return
                    
                    
                    end = start + datetime.timedelta(minutes=30)
                    #self.say(f"does this sound right? '{title}' at {start.strftime('%Y-%m-%d %H:%M')}")
                    add_event(title, start.isoformat(), end.isoformat())
                    self.say("Event scheduled!")
                    
                elif 101 == code:
                    self.say("Exiting.")
                    return

                elif code == 102:
                    title = response.split("-:-")[0]
                    content = response.split("-:-")[1]
                    googledochelper.create_and_write_doc(title, content)
                    self.say(f"Document '{title}' made")
                elif 103 == code:
                    parts = [p.strip() for p in response.split(",")]
                    title = parts[0] if len(parts) > 0 else ""
                    notes = parts[1] if len(parts) > 1 and parts[1].lower() != "empty" else None
                    due_date_str = parts[2] if len(parts) > 2 and parts[2].lower() != "empty" else None
                    due_date = dateparser.parse(due_date_str).isoformat() if due_date_str else None

                        
                    service = googleToDo.get_tasks_service()
                    task_lists = service.tasklists().list().execute()
                    default_list_id = task_lists['items'][0]['id']
                    googleToDo.add_task(service, default_list_id, title, notes, due_date)
                    self.say(f"Task '{title}' added to your to-do list.")
                elif 104 == code:
                    
                    service = googleToDo.get_tasks_service()
                    task_lists = service.tasklists().list().execute()
                    default_list_id = task_lists['items'][0]['id']
                    tasks = googleToDo.list_tasks(service, default_list_id)
                    if tasks:
                        self.say("Listing your tasks:")
                        for task in tasks:
                            self.say(f" - {task['title']}")
                    else:
                        self.say("You have no tasks in your to-do list.")
                elif 105 == code:
                    task_title = response
                    service = googleToDo.get_tasks_service()
                    task_lists = service.tasklists().list().execute()
                    default_list_id = task_lists['items'][0]['id']
                    tasks = googleToDo.list_tasks(service, default_list_id)
                    task_found = False
                    for task in tasks:
                        if task['title'].lower() == task_title.lower():
                            googleToDo.complete_task(service, default_list_id, task['id'])
                            self.say(f"Task '{task_title}' marked as completed.")
                            task_found = True
                            break
                    if not task_found:
                        self.say(f"Task '{task_title}' not found.")
                elif 106 == code:
                    self.say("Taking selfie.")
                    camera = Camera()
                    frame = camera.take_selfie()
                    self.game_view.show_frame(frame)
                elif 108 == code:
                    self.say("sorry, i didn't understand that")
                elif 109 == code:
                    self.say(response)
                elif 110 == code:
                    self.say("Focus mode activated. I will minimize distractions.")
                    ps.playsound("audio/focusApe.mp3")
                    #TODO: Implement focus mode logic


    def run(self):
        try:
            self.mic = sr.Microphone()
        except Exception as e:
            print(f"Microphone initialization failed: {e}")
            self.mic = None

        if self.mic is None:
            print("Microphone not initialized. Please check your setup.")
            return
        while True and not self.stop_flag:
            if not self.game_view.isChatopen and self.listen_for_wake_word():
                user_command = self.listen_for_command()
                response = self.llm.ask_ollama( "TODAYS DAY AND TIME FOR THE USER: ["+ datetime.datetime.now().isoformat() + "]" + user_command)
                code = int(response[:5].replace("[", "").replace("]", ""))
                response = response[5:]
                print("LLM Response:", response)
                
                self.handle_code(code, response)
                   