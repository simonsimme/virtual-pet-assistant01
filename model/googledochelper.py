from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path
import pickle
import sys

SCOPES = ['https://www.googleapis.com/auth/documents']

def get_docs_service():
    creds = None
    if os.path.exists('token_docs.pickle'):
        with open('token_docs.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                get_resource_path('model/credentials.json'), SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token_docs.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('docs', 'v1', credentials=creds)
    return service
def get_resource_path(relative_path):
        """Get the absolute path to a resource, works for dev and PyInstaller."""
        if getattr(sys, 'frozen', False):  # Check if running as a PyInstaller bundle
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

def create_and_write_doc(title, text):
    service = get_docs_service()
    # Create a new document
    doc = service.documents().create(body={'title': title}).execute()
    doc_id = doc.get('documentId')
    # Write text to the document
    requests = [
        {
            'insertText': {
                'location': {
                    'index': 1,
                },
                'text': text
            }
        }
    ]
    service.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()
    print(f"Created document: https://docs.google.com/document/d/{doc_id}/edit")

# Example usage:
# create_and_write_doc("My Pet Note", "This is a note from my virtual pet assistant!")