# 🐾 Virtual Pet Assistant

## 📖 Overview
The **Virtual Pet Assistant** is an interactive application that simulates a virtual pet experience. It combines gameplay elements with productivity features, such as scheduling tasks and reminders, making it both entertaining and functional.

As you care for your pet, you can manage its hunger, mood, energy, cleanliness, and health. The application includes various activities like feeding, cleaning, exploring, and playing with your pet. It also features dynamic animations that reflect your pet's state and activities.

This assistant can also help you manage your tasks and events by integrating with Google Calendar and Google Tasks. You can control the assistant using voice commands or a chat interface, making it easy to interact with your virtual pet.

With local LLM integration, the assistant can provide intelligent responses and suggestions without the need for an internet connection.

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
- Ollama: LLM api integration, LLM used is Mistral instruct.
---

## Installation
- Download ollama, www.ollama.com 
- Download the git project
- Runfile located in **dist** folder, in this folder run main.exe

---
## Usage
- Run main.exe in the dist folder
## LLM Usage
- the mic is always on, the speech recognition is listening for you to say "Hey" + (name of your pet), the command line will print out what the recognition heard
- The LLM uses local computing capabilities, so the response time will vary depending on your computer. For older computers, response time can be up to 5 minutes. If you have too low memory for Mistral, it's possible to change what LLM model is being used, but not recommended. It's changeable in the ollama.py script.
- It's also possible to chat with the LLM by clicking on the keyboard button.
---


## 🎮 Welcome to Your Virtual Cat Companion (Game Introduction)

Start by selecting your **virtual cat** and giving it a name.  
> ⚠️ This name is voice-activated and used when interacting with the AI — choose wisely!

![Cat Selection](https://github.com/user-attachments/assets/50e71448-f730-4145-8a5a-63ee0318db26)

---

### 🧼 Caring for Your Pet

- Keep your cat's **stats from getting too low** to help it grow and survive.
- To **clean** your cat, press the **🧽 brush button**, then **hold mouse 1 and drag across the cat**.
- A **red text** above the brush shows the **cooldown timer**.

![Cleaning](https://github.com/user-attachments/assets/ba877fdd-c55c-41fe-955e-0759b74238a8)

---

### 🧭 Exploring & Feeding

- Press the **🗺️ map button** to send your cat out exploring.
- It may return with **food**, which is stored in your **🎒 inventory** (accessed via the **bag icon**).

![Exploring](https://github.com/user-attachments/assets/3bc3cef9-a994-4c88-bf91-22df54884d2c)

---

### 💬 Chatting with Your Cat

- Use **voice commands** to talk to your cat.
- You can also use the **⌨️ keyboard button** to access the AI chat manually.
- Tap the **ℹ️ info icon** for a quick list of non-AI commands (faster and lower latency).

![Chat UI](https://github.com/user-attachments/assets/9cd8108a-2285-4132-86f4-3286c6f4439c)

---

### 💀 Game Over & High Score

If your pet dies, its **age will be saved as a high score**.  
You can then **create a new cat** and try to beat your previous record!

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
