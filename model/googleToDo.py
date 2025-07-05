from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
import os

SCOPES = ['https://www.googleapis.com/auth/tasks']

def get_tasks_service():
    creds = None
    if os.path.exists('token_tasks.pickle'):
        with open('token_tasks.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            os.path.join(os.path.dirname(__file__), 'credentials.json'), SCOPES)
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