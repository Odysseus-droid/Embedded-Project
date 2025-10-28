import os
import threading
from firebase_admin import db, credentials, initialize_app
import firebase_admin

# Load Firebase credentials and database URL from environment variables
GOOGLE_CRED_PATH = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
FIREBASE_DATABASE_URL = os.environ.get('FIREBASE_DATABASE_URL')

# Initialize Firebase
try:
    firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate(GOOGLE_CRED_PATH)
    initialize_app(cred, options={'databaseURL': FIREBASE_DATABASE_URL})


def listen_to_rfid_taps(callback):
    """Listen to RFID tap events"""
    ref = db.reference('rfid_taps')

    def on_change(message):
        try:
            print(f"[Firebase Listener] RFID Tap detected: {message.data}")
            if callback:
                callback(message.data)
        except Exception as e:
            print(f"[RFID Listener] Error: {e}")

    try:
        ref.listen(on_change)
    except Exception as e:
        print(f"[RFID Listener] Listener failed: {e}")


def listen_to_flood_sensor(callback):
    """Listen to flood sensor updates"""
    ref = db.reference('flood_sensor')

    def on_change(message):
        try:
            print(f"[Firebase Listener] Flood sensor update: {message.data}")
            if callback:
                callback(message.data)
        except Exception as e:
            print(f"[Flood Listener] Error: {e}")

    try:
        ref.listen(on_change)
    except Exception as e:
        print(f"[Flood Listener] Listener failed: {e}")


def listen_to_servo_commands(callback):
    """Listen to servo gate commands"""
    ref = db.reference('servo_commands')

    def on_change(message):
        try:
            print(f"[Firebase Listener] Servo command: {message.data}")
            if callback:
                callback(message.data)
        except Exception as e:
            print(f"[Servo Listener] Error: {e}")

    try:
        ref.listen(on_change)
    except Exception as e:
        print(f"[Servo Listener] Listener failed: {e}")


def start_listeners():
    """Start all Firebase listeners in background threads"""

    def rfid_callback(data):
        print(f"[RFID Callback] Processing RFID tap: {data}")
        # TODO: integrate with your entry_gate/exit_gate API

    def flood_callback(data):
        print(f"[Flood Callback] Processing flood data: {data}")
        # TODO: trigger emergency override if threshold exceeded

    def servo_callback(data):
        print(f"[Servo Callback] Processing servo command: {data}")
        # TODO: integrate with hardware API to move gate

    threading.Thread(target=listen_to_rfid_taps, args=(rfid_callback,), daemon=True).start()
    threading.Thread(target=listen_to_flood_sensor, args=(flood_callback,), daemon=True).start()
    threading.Thread(target=listen_to_servo_commands, args=(servo_callback,), daemon=True).start()

    print("[Firebase] All listeners started")
