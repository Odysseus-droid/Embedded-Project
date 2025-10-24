import time
from toll_system.models import RFID, Transaction, FloodLog
from django.conf import settings
from .firebase_publisher import push_servo_command, push_emergency_override
import pyrebase
import os, django

# Setup Django environment so this script can access models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expressway_project.settings')
django.setup()

# Initialize Firebase
firebase = pyrebase.initialize_app(settings.FIREBASE_CONFIG)
db = firebase.database()

# --- HANDLERS ---
def handle_rfid_tap(message):
    data = message['data']
    event = message['event']

    if event == 'put' and data:
        rfid_id = data.get('rfid_id')
        tap_type = data.get('type') # e.g., "ENTRY" or "EXIT"

        # 1. Look up RFID and check balance/status
        try:
            rfid = RFID.objects.get(rfid_id=rfid_id)

            if tap_type == 'ENTRY':
                if rfid.value_balance >= settings.MINIMUM_ENTRY_BALANCE:
                    # Create Transaction object (time_in)
                    push_servo_command(rfid_id, "OPEN")
                else:
                    push_servo_command(rfid_id, "BLOCKED")

            elif tap_type == 'EXIT':
                # Find open transaction, calculate toll, deduct balance, close transaction
                push_servo_command(rfid_id, "OPEN")

        except RFID.DoesNotExist:
            push_servo_command(rfid_id, "BLOCKED")

def handle_flood_sensor(message):
    data = message['data']
    if message['event'] == 'put' and data:
        water_level = data.get('level', 0)

        if water_level >= settings.CRITICAL_FLOOD_LEVEL:
            push_emergency_override("ACTIVE")
            FloodLog.objects.create(water_level=water_level, action_taken="EMERGENCY TOLL OPEN")
        elif water_level < settings.CRITICAL_FLOOD_LEVEL - 10: # Hysteresis to prevent flicking
            push_emergency_override("INACTIVE")

# --- STREAMING START ---
def start_listeners():
    # Start listening to taps
    db.child("realtime_taps").stream(handle_rfid_tap)

    # Start listening to flood sensor
    db.child("flood_sensor/status").stream(handle_flood_sensor)

if __name__ == '__main__':
    print("Starting Firebase Listeners...")
    start_listeners()