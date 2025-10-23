import pyrebase
from django.conf import settings

# Initialize Firebase using settings from settings.py
firebase = pyrebase.initialize_app(settings.FIREBASE_CONFIG)
db = firebase.database()

def push_servo_command(rfid_id, command):
    # Logic to write OPEN/BLOCKED command to /servo_commands/entrance/{rfid_id}
    db.child(f"servo_commands/entrance/{rfid_id}").set({"command": command, "timestamp": pyrebase.firebase_datetime.now()})

def push_emergency_override(status):
    # Logic to write ACTIVE/INACTIVE command to /global_commands/emergency_override
    db.child("global_commands/emergency_override").set({"status": status, "reason": "FLOOD"})