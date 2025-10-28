from django.db import models
from django.utils import timezone

class RFIDAccount(models.Model):
    VEHICLE_TYPES = [
        ('public', 'Public'),
        ('private', 'Private'),
        ('emergency', 'Emergency'),
    ]

    ROLE_TYPES = [
        ('adult', 'Adult'),
        ('non-adult', 'Non-Adult'),
        ('deceased', 'Deceased'),
    ]

    rfid_uid = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_TYPES, default='adult')
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPES, default='public')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.rfid_uid}) - ₱{self.balance}"

    class Meta:
        db_table = 'rfid_accounts'


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('entry', 'Entry'),
        ('exit', 'Exit'),
        ('topup', 'Top-Up'),
    ]

    rfid_account = models.ForeignKey(RFIDAccount, on_delete=models.CASCADE, related_name="transactions")
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    gate_id = models.CharField(max_length=20, default='gate1')
    old_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    new_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    amount_changed = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type.upper()} | {self.rfid_account.name} | ₱{self.amount_changed} | {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"

    class Meta:
        db_table = 'transactions'
        ordering = ['-timestamp']


class FloodSensor(models.Model):
    water_level = models.FloatField(default=0.0)
    is_emergency = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Water Level: {self.water_level}% - Emergency: {self.is_emergency}"

    class Meta:
        db_table = 'flood_sensors'
        ordering = ['-timestamp']
