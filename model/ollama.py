import requests
import subprocess

class LLM:
    def __init__(self, petname):
        self.petname = petname
        self.initialize_ollama()

    def initialize_ollama(self):
        """Start the Ollama server if it's not already running."""
        try:
            # Try a simple request to see if Ollama is running
            requests.get("http://localhost:11434")
        except Exception:
            try:
                subprocess.Popen(["ollama", "serve"])
                print("Ollama server started.")
            except Exception as e:
                print("Could not start Ollama server:", e)

    def ask_ollama(self, prompt, model="mistral:instruct"):
        SYSTEM_PROMPT = (
    "You are a friendly virtual pet assistant. "
    "For all questions, respond shortly and clearly. "
    "the user can ask you to the following and i want you to respond in acordance with the code first of your response like this [CODE]:"
    "[100] for schedule an event, in this way: [100] event name, date . EXAMPLE: [100] Meeting with John, tomorrow at 10. if no date is provided, use 'EMPTY' for that field. Use this if the user want to scheduale some event"
    "[101] if the user just says exit/want to end the conversation, just return the code like this: [101]"
    "[102] for make a document, in this way: [102] document title -:- document content."
    "[103] for add a task, in this way: [103] task title, task notes, due date. EXAMPLE: [103] Buy groceries, Remember to buy milk and eggs, today at 10. if no date/notes are provided, use 'EMPTY' for those fields. Only use this if user mentions todo/task"
    "[104] for list tasks. this is the list of todo task the user has, if you think the user wants to know all their todo tasks respond like this: [104]."
    "[105] for complete a todo task, if the user tells you he as completed a todo task respond in this way: [105] task title."
    "[106] for take a selfie, if the user says to take a selfie respond in this way: [106]."
    "[107] for exit, if the user says to exit respond in this way: [107]."
    "[108] for repromt (if you want the user to repeat the statement or question). respond in this way: [108]."
    "[109] if the user asks you a question or statement outside the commands, you can give a fitting respons formated like this: [109] your response here. this can for example be if the user asks for the weather, in this way: [109] your response here."
    "[110] if the user asks you to turn on focus mode, respond in this way: [110]."
    "stick to the format of the commands if one feild is missing from the user input write: 'EMPTY' in its place. Do not add in you on words or explanations, just respond with the code and the format."
    "its very importat that you follow the codes, all regular questions should be answered with the code [109]. "
    "i will send in previous conversations, but just focus on the new user command"
    
)
        petname_add = "Your pet name is " + self.petname + ". "
        SYSTEM_PROMPT = petname_add + SYSTEM_PROMPT
        full_prompt = f"{SYSTEM_PROMPT}\nUser: {prompt}:"
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": full_prompt, "stream": False}
        )
        #print(response.status_code, response.text)
        return response.json()["response"].strip()
    
    def stop_ollama():
        try:
            subprocess.Popen(["ollama", "stop"])
        except Exception as e:
            print("Could not stop Ollama:", e)


