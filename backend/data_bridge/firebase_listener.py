import firebase_admin
from firebase_admin import db
import threading
import time

# HARDCODED: Firebase configuration - same as publisher
FIREBASE_CONFIG = {
    'databaseURL': 'YOUR_DATABASE_URL'
}

# Initialize Firebase
try:
    firebase_admin.get_app()
except ValueError:
    firebase_admin.initialize_app(options={
        'databaseURL': FIREBASE_CONFIG['databaseURL']
    })


def listen_to_rfid_taps(callback):
    """
    Listen to RFID tap events from IoT devices
    
    Args:
        callback: Function to call when new tap is detected
    """
    ref = db.reference('rfid_taps')
    
    def on_change(message):
        print(f"[Firebase Listener] RFID Tap detected: {message.data}")
        if callback:
            callback(message.data)
    
    ref.listen(on_change)


def listen_to_flood_sensor(callback):
    """
    Listen to flood sensor updates
    
    Args:
        callback: Function to call when flood level changes
    """
    ref = db.reference('flood_sensor')
    
    def on_change(message):
        print(f"[Firebase Listener] Flood sensor update: {message.data}")
        if callback:
            callback(message.data)
    
    ref.listen(on_change)


def listen_to_servo_commands(callback):
    """
    Listen to servo gate commands
    
    Args:
        callback: Function to call when servo command is received
    """
    ref = db.reference('servo_commands')
    
    def on_change(message):
        print(f"[Firebase Listener] Servo command: {message.data}")
        if callback:
            callback(message.data)
    
    ref.listen(on_change)


def start_listeners():
    """Start all Firebase listeners in background threads"""
    
    def rfid_callback(data):
        print(f"Processing RFID tap: {data}")
        # HARDCODED: Add your RFID processing logic here
        # Example: Call entry_gate or exit_gate API based on tap location
    
    def flood_callback(data):
        print(f"Processing flood data: {data}")
        # HARDCODED: Add your flood processing logic here
        # Example: Trigger emergency override if water level exceeds threshold
    
    # Start listeners in separate threads
    threading.Thread(target=listen_to_rfid_taps, args=(rfid_callback,), daemon=True).start()
    threading.Thread(target=listen_to_flood_sensor, args=(flood_callback,), daemon=True).start()
    threading.Thread(target=listen_to_servo_commands, args=(None,), daemon=True).start()
    
    print("[Firebase] All listeners started")
