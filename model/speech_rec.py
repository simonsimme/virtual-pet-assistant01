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
# Load spaCy English model (download with: python -m spacy download en_core_web_sm)
nlp = spacy.load("en_core_web_sm")

class SpeechAssistant:
    def say(self, text):
        """Use text-to-speech to say the given text."""
        if self.game_view.isChatopen:
            self.game_view.pet_chat_response(text)
        else:
            self.engine.say(text)
            self.engine.runAndWait()

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

    def extract_event_info(self, command):
        # Remove trigger words
        for trigger in ["add event", "schedule event"]:
            if trigger in command:
                command = command.replace(trigger, "")
        doc = nlp(command)
        ents = [ent for ent in doc.ents if ent.label_ in ("DATE", "TIME")]
        if ents:
            # Find the first group of consecutive DATE/TIME entities
            start_idx = ents[0].start
            end_idx = ents[0].end
            for i in range(1, len(ents)):
                if ents[i].start == end_idx:
                    end_idx = ents[i].end
                else:
                    break
            date_phrase = doc[start_idx:end_idx].text
            event_time = dateparser.parse(date_phrase)
            # The title is everything after the date phrase
            title = doc[end_idx:].text.strip()
            if not title:
                # fallback: everything except date_phrase
                title = command.replace(date_phrase, "").strip()
        else:
            event_time = datetime.datetime.now() + datetime.timedelta(minutes=1)
            title = command.strip()
        return title, event_time

    
    def handle_response_text(self, user_command):
                response = self.llm.ask_ollama( "TODAYS DAY AND TIME FOR THE USER: ["+ datetime.datetime.now().isoformat() + "]" + user_command)
                code = int(response[:5].replace("[", "").replace("]", ""))
                response = response[5:]
                print("LLM Response:", response)
                print(f"Code: {code}")
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
                    self.game_view.show_frame(frame, self.screen)
                elif 108 == code:
                    self.say("sorry, i didn't understand that")
                elif 109 == code:
                    self.say(response)
                elif 110 == code:
                    self.say("Focus mode activated. I will minimize distractions.")
                    ps.playsound("audio/focusApe.mp3")
                    #TODO: Implement focus mode logic


    def run(self):
        if self.mic is None:
            print("Microphone not initialized. Please check your setup.")
            return
        continue_running = False
        while True:
            if not self.game_view.isChatopen and self.listen_for_wake_word():
                user_command = self.listen_for_command()
                response = self.llm.ask_ollama(user_command)
                code = int(response[:5].replace("[", "").replace("]", ""))
                response = response[5:]
                print("LLM Response:", response)
                
                if code == 100:
                    # Extract event info from the full command
                    parts = response.split(",")
                    title = parts[0].strip() if len(parts) > 0 else ""
                    if len(parts) == 2 and "T" in parts[1]:
                        # Handle ISO 8601 combined date and time
                        dt = dateparser.parse(parts[1].strip())
                        date_str = dt.strftime("%Y-%m-%d") if dt else ""
                        time_str = dt.strftime("%H:%M") if dt else ""
                    else:
                        date_str = parts[1].strip() if len(parts) > 1 else ""
                        time_str = parts[2].strip() if len(parts) > 2 else ""
                    start = dateparser.parse(f"{date_str} {time_str}")
                    
                    if title == "EMPTY":
                        self.say("Could not extract event title. Please try again.")
                        continue
                    if "EMPTY" == start:
                        self.say("Could not understand the date/time.")
                        continue
                    end = start + datetime.timedelta(minutes=30)
                    self.say(f"does this sound right? '{title}' at {start.strftime('%Y-%m-%d %H:%M')}")
                    user_confirmation = self.listen_for_command()
                    if "yes" in user_confirmation or "sure" in user_confirmation or "okay" in user_confirmation or "yep" in user_confirmation:
                        add_event(title, start.isoformat(), end.isoformat())
                        self.say("Event scheduled!")
                    else:
                        self.say("Event scheduling canceled.")
                elif 101 == code:
                    self.say("Exiting.")
                    break
                elif code == 102:
                    title = response.split("-:-")[0]
                    content = response.split("-:-")[1]
                    googledochelper.create_and_write_doc(title, content)
                    self.say(f"Document '{title}' made")
                elif 103 == code:
                    task_title = response.split(",")[0]
                    notes = response.split(",")[1]
                    due_date = response.split(",")[2]
                    
                    if due_date.lower() == "EMPTY":
                        due_date = None
                    else:
                        try:
                            due_date = dateparser.parse(due_date).isoformat()
                        except Exception as e:
                            self.say("Invalid date format. Task will be added without a due date.")
                            due_date = None
                    service = googleToDo.get_tasks_service()
                    task_lists = service.tasklists().list().execute()
                    default_list_id = task_lists['items'][0]['id']
                    googleToDo.add_task(service, default_list_id, title, notes, due_date)
                    self.say(f"Task '{title}' added to your to-do list.")
                elif 104 == code:
                    self.say("Listing your tasks.")
                    service = googleToDo.get_tasks_service()
                    task_lists = service.tasklists().list().execute()
                    default_list_id = task_lists['items'][0]['id']
                    tasks = googleToDo.list_tasks(service, default_list_id)
                    for task in tasks:
                        self.say(task['title'])
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
                    self.game_view.show_frame(frame, self.screen)
                elif 108 == code:
                    self.say("sorry, i didn't understand that")
                elif 109 == code:
                    self.say(response)
                elif 110 == code:
                    self.say("Focus mode activated. I will minimize distractions.")
                    ps.playsound("audio/focusApe.mp3")
                    #TODO: Implement focus mode logic
                   