# 🐾 Virtual Pet Assistant

## 📖 Overview
The **Virtual Pet Assistant** is an interactive application that simulates a virtual pet experience. It combines gameplay elements with productivity features, such as scheduling tasks and reminders, making it both entertaining and functional.

As you care for your pet, you can manage its hunger, mood, energy, cleanliness, and health. The application includes various activities like feeding, cleaning, exploring, and playing with your pet. It also features dynamic animations that reflect your pet's state and activities.

This assistant can also help you manage your tasks and events by integrating with Google Calendar and Google Tasks. You can control the assistant using voice commands or a chat interface, making it easy to interact with your virtual pet.

With local LLM integration, the assistant can provide intelligent responses and suggestions, without the need for an internet connection.

Pick the name and appearance of your pet, and enjoy a personalized experience. 

---

## ✨ Features
- 🐕 **Virtual Pet Simulation**: Manage your pet's hunger, mood, growth, energy, cleanliness, and health.
- 🎮 **Interactive Activities**: Feed, clean and explore.
- 🎥 **Dynamic Animations**: Real-time animations based on your pet's state and activities.
- 📅 **Task Scheduling**: Add events and tasks to Google Calendar and Google Tasks.
- 🎙️ **Voice Commands**: Control the assistant using speech recognition.
- 💬 **Chat Interaction**: Communicate with your pet via a chat interface.
- 📸 **Selfie Mode**: Take selfies with your pet using your webcam. *(Not yet implemented)*
- 💾 **Save and Load**: Persistent pet state across sessions.
- 🏆 **Highscore**: Tracks the pet's age as a highscore.
- 🎨 **Customizable Pets**: Choose your pet's appearance and name.
- 🎵 **Focus Mode**: Turns on focus music for productivity.

---
## 🛠️ Technologies Used
- Python: Core programming language.
- Pygame: For GUI and animations.
- Google APIs: Integration with Calendar, Tasks, and Docs.
- SpeechRecognition: For voice commands.
- OpenCV: For webcam functionality.
- Ollama: LLM api integration, LLM used is Mistral 7B.
---

## Installation
- Download ollama, www.ollama.com 
- Download the git project
- Runfile located in **dist** folder, in this folder run main.exe

---
## Usage
- Run main.exe in the dist folder
## LLM Usage
-
---

## 🎮 Game Introduction
- Start by selecting your virtual cat and giving it a name. Be careful of what name you choose, as that name is used when needing to start a dialog with the LLM and is voice-activated
- <img width="1915" height="812" alt="Skärmbild 2025-08-06 102122" src="https://github.com/user-attachments/assets/50e71448-f730-4145-8a5a-63ee0318db26" />
- Your virtual pet will grow over time, but to keep it alive, you need to make sure its stats don't get too low. The keyboard button is to access the LLM chat instead of voice recognition, and the info icon contains a list of commands that don't go to the LLM for quicker latency.
- <img width="521" height="555" alt="Skärmbild 2025-08-05 145433" src="https://github.com/user-attachments/assets/9cd8108a-2285-4132-86f4-3286c6f4439c" />
- You clean the cat by pressing the brush and then holding mouse 1 and dragging across the pet, the red text over the brush button is the brush cooldown
-<img width="1121" height="841" alt="Skärmbild 2025-08-05 145654" src="https://github.com/user-attachments/assets/ba877fdd-c55c-41fe-955e-0759b74238a8" />
- To acquire food, you will need to let your cat explore. Do this by pressing the map button. The food it finds will be placed in the inventory accessible from the bag button.
-<img width="1125" height="838" alt="Skärmbild 2025-08-05 145559" src="https://github.com/user-attachments/assets/3bc3cef9-a994-4c88-bf91-22df54884d2c" />

- If your pet dies, the age will be saved as the high score and will allow you to remake your pet and try again.





---
## 🗂️ Code Structure
- main.py: Entry point for the application.
- model/: Contains core logic for pet behavior, Google API integration, and state management.
- view/: Handles the graphical user interface and animations.
- controller/: Manages user input and interactions.
- assets/: Includes pet animations and icons.
---

## 🚧 Future Improvements

---
## 🔒 License
This project is proprietary and not open-source. All rights are reserved. You may not copy, modify, distribute, or use this project without explicit permission from the author.
