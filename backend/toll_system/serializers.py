from rest_framework import serializers
from .models import RFID, Transaction

class RFIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFID
        fields = ['rfid_id', 'owner_name', 'value_balance', 'car_type']

class TopUpSerializer(serializers.Serializer):
    # Defines the required input for the TopUp API endpoint
    rfid_id = serializers.CharField(max_length=50)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)