from django.db import models

class RFID(models.Model):
    # ... (Fields: rfid_id, owner_name, value_balance, car_type, is_active)
    pass

class Transaction(models.Model):
    # ... (Fields: rfid FK, time_in, time_out, toll_fee, entry_authorized, current_status)
    pass

class FloodLog(models.Model):
    # ... (Fields: timestamp, water_level, action_taken)
    pass