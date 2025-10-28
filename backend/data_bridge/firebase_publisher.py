import firebase_admin
from firebase_admin import db
import json
from datetime import datetime

# HARDCODED: Firebase configuration - replace with your credentials
FIREBASE_CONFIG = {
    'apiKey': 'YOUR_API_KEY',
    'authDomain': 'YOUR_AUTH_DOMAIN',
    'databaseURL': 'YOUR_DATABASE_URL',
    'projectId': 'YOUR_PROJECT_ID',
    'storageBucket': 'YOUR_STORAGE_BUCKET',
    'messagingSenderId': 'YOUR_MESSAGING_SENDER_ID',
    'appId': 'YOUR_APP_ID'
}

# Initialize Firebase (only once)
try:
    firebase_admin.get_app()
except ValueError:
    firebase_admin.initialize_app(options={
        'databaseURL': FIREBASE_CONFIG['databaseURL']
    })


def publish_to_firebase(path, data):
    """
    Publish data to Firebase Realtime Database
    
    Args:
        path: Firebase path (e.g., 'real_time_taps', 'rfid_data', 'flood_sensor')
        data: Dictionary to publish
    """
    try:
        ref = db.reference(path)
        ref.push(data)
        print(f"[Firebase] Published to {path}: {data}")
    except Exception as e:
        print(f"[Firebase Error] Failed to publish to {path}: {str(e)}")


def update_rfid_status(rfid_uid, status, location):
    """
    Updated to use rfid_uid instead of rfid_code
    Update RFID status in Firebase
    """
    data = {
        'rfid_uid': rfid_uid,
        'status': status,
        'location': location,
        'timestamp': datetime.now().isoformat()
    }
    publish_to_firebase('rfid_status', data)


def trigger_emergency_override():
    """Trigger emergency override for all gates"""
    data = {
        'emergency_active': True,
        'timestamp': datetime.now().isoformat(),
        'message': 'All tolls waived - Emergency evacuation in progress'
    }
    publish_to_firebase('global_commands', data)
