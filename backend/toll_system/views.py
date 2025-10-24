from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import RFID
from .serializers import TopUpSerializer

class TopUpView(APIView):
    def put(self, request, *args, **kwargs):
        serializer = TopUpSerializer(data=request.data)
        if serializer.is_valid():
            rfid_id = serializer.validated_data['rfid_id']
            amount = serializer.validated_data['amount']

            try:
                with transaction.atomic():
                    rfid = RFID.objects.select_for_update().get(rfid_id=rfid_id)
                    rfid.value_balance += amount
                    rfid.save()
                    return Response({"status": "success", "new_balance": rfid.value_balance}, status=status.HTTP_200_OK)
            except RFID.DoesNotExist:
                return Response({"error": "RFID not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)