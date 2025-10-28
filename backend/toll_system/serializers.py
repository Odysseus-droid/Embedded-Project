from rest_framework import serializers
from .models import RFIDAccount, Transaction, FloodSensor

class RFIDAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFIDAccount
        fields = ['id', 'rfid_uid', 'name', 'role', 'vehicle_type', 'balance', 'created_at']
        read_only_fields = ['created_at']


class TransactionSerializer(serializers.ModelSerializer):
    rfid_name = serializers.CharField(source='rfid_account.name', read_only=True)
    rfid_uid = serializers.CharField(source='rfid_account.rfid_uid', read_only=True)
    vehicle_type = serializers.CharField(source='rfid_account.vehicle_type', read_only=True)
    old_balance = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    new_balance = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    amount_changed = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'rfid_uid', 'rfid_name', 'vehicle_type', 'transaction_type', 'gate_id', 
                  'old_balance', 'new_balance', 'amount_changed', 'timestamp']
        read_only_fields = ['timestamp', 'old_balance', 'new_balance', 'transaction_type', 'gate_id']



class FloodSensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = FloodSensor
        fields = ['id', 'water_level', 'is_emergency', 'timestamp']
        read_only_fields = ['timestamp']
