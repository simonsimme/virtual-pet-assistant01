from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
import os
import sys

SCOPES = ['https://www.googleapis.com/auth/tasks']

def get_resource_path(relative_path):
        """Get the absolute path to a resource, works for dev and PyInstaller."""
        if getattr(sys, 'frozen', False):  # Check if running as a PyInstaller bundle
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

def get_tasks_service():
    creds = None
    if os.path.exists('token_tasks.pickle'):
        with open('token_tasks.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            get_resource_path('model/credentials.json'), SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token_tasks.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('tasks', 'v1', credentials=creds)
    return service
def complete_task(service, task_list_id, task_id):
    service.tasks().patch(tasklist=task_list_id, task=task_id, body={'status': 'completed'}).execute()
    print("Task marked as completed.")
    
def list_tasks(service, task_list_id):
    results = service.tasks().list(tasklist=task_list_id).execute()
    tasks = results.get('items', [])
    for task in tasks:
        print(task['title'])
    return tasks
    
        
def add_task(service, task_list_id, title, notes=None, due=None):
    task = {'title': title}
    if notes:
        task['notes'] = notes
    if due:
        task['due'] = due  # ISO 8601 format
    result = service.tasks().insert(tasklist=task_list_id, body=task).execute()
    print(f"Task added: {result['title']}")