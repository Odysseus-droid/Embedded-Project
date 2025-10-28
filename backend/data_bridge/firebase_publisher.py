import os
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

# Read from environment variables
FIREBASE_DATABASE_URL = os.getenv('FIREBASE_DATABASE_URL')
GOOGLE_CRED_PATH = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

if not FIREBASE_DATABASE_URL or not GOOGLE_CRED_PATH:
    raise ValueError("Firebase URL or credentials path not set in environment variables")

# Initialize Firebase
try:
    firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate(GOOGLE_CRED_PATH)
    firebase_admin.initialize_app(cred, {
        'databaseURL': FIREBASE_DATABASE_URL
    })

def publish_to_firebase(path, data):
    ref = db.reference(path)
    ref.push(data)
    print(f"[Firebase] Published to {path}: {data}")

def update_rfid_status(rfid_uid, status, location):
    data = {
        'rfid_uid': rfid_uid,
        'status': status,
        'location': location,
        'timestamp': datetime.now().isoformat()
    }
    publish_to_firebase('rfid_status', data)

def trigger_emergency_override():
    data = {
        'emergency_active': True,
        'timestamp': datetime.now().isoformat(),
        'message': 'All tolls waived - Emergency evacuation in progress'
    }
    publish_to_firebase('global_commands', data)
