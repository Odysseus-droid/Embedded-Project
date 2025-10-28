from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.db.models import Sum
from django.http import HttpResponse
from django.db import transaction

from .models import RFIDAccount, Transaction, FloodSensor
from .serializers import RFIDAccountSerializer, TransactionSerializer, FloodSensorSerializer
from data_bridge.firebase_publisher import publish_to_firebase

# Constants
EMERGENCY_WATER_LEVEL = 80.0
MINIMUM_BALANCE_FOR_ENTRY = 10.0
TOLL_RATES = {
    'public': 50.0,
    'private': 75.0,
    'emergency': 0.0,
}

# -----------------------------
# Template / HTML Views
# -----------------------------
class DashboardView(View):
    def get(self, request):
        total_rfids = RFIDAccount.objects.count()
        total_balance = RFIDAccount.objects.aggregate(Sum('balance'))['balance__sum'] or 0
        today = timezone.now().date()
        today_transactions = Transaction.objects.filter(timestamp__date=today)
        today_revenue = today_transactions.filter(transaction_type='exit').aggregate(Sum('amount_changed'))['amount_changed__sum'] or 0
        recent_transactions = Transaction.objects.all().order_by('-timestamp')[:10]
        latest_flood = FloodSensor.objects.latest('timestamp') if FloodSensor.objects.exists() else None

        return render(request, 'toll_system/dashboard.html', {
            'total_rfids': total_rfids,
            'total_balance': total_balance,
            'today_revenue': today_revenue,
            'recent_transactions': recent_transactions,
            'latest_flood': latest_flood,
        })


class RFIDListView(View):
    def get(self, request):
        rfid_accounts = RFIDAccount.objects.all()
        return render(request, 'toll_system/rfid_list.html', {'rfid_accounts': rfid_accounts})


class RFIDDetailView(View):
    def get(self, request, rfid_uid):
        rfid_account = get_object_or_404(RFIDAccount, rfid_uid=rfid_uid)
        transactions = Transaction.objects.filter(rfid_account=rfid_account).order_by('-timestamp')[:20]
        return render(request, 'toll_system/rfid_detail.html', {
            'rfid_account': rfid_account,
            'transactions': transactions,
        })


class TransactionListView(View):
    def get(self, request):
        transactions = Transaction.objects.all().order_by('-timestamp')[:100]
        return render(request, 'toll_system/transaction_list.html', {'transactions': transactions})


class SystemStatusView(View):
    def get(self, request):
        total_rfids = RFIDAccount.objects.count()
        emergency_vehicles = RFIDAccount.objects.filter(vehicle_type='emergency').count()
        public_vehicles = RFIDAccount.objects.filter(vehicle_type='public').count()
        private_vehicles = RFIDAccount.objects.filter(vehicle_type='private').count()
        total_transactions = Transaction.objects.count()
        total_revenue = Transaction.objects.filter(transaction_type='exit').aggregate(Sum('amount_changed'))['amount_changed__sum'] or 0
        latest_flood = FloodSensor.objects.latest('timestamp') if FloodSensor.objects.exists() else None

        return render(request, 'toll_system/system_status.html', {
            'total_rfids': total_rfids,
            'emergency_vehicles': emergency_vehicles,
            'public_vehicles': public_vehicles,
            'private_vehicles': private_vehicles,
            'total_transactions': total_transactions,
            'total_revenue': total_revenue,
            'latest_flood': latest_flood,
        })


class StatusView(View):
    def get(self, request):
        return render(request, 'toll_system/status.html')


def home(request):
    return HttpResponse("Expressway Backend is Running!")


# -----------------------------
# API ViewSets
# -----------------------------
class RFIDAccountViewSet(viewsets.ModelViewSet):
    queryset = RFIDAccount.objects.all()
    serializer_class = RFIDAccountSerializer

    @action(detail=False, methods=['post'])
    def topup(self, request):
        rfid_uid = request.data.get('rfid_uid')
        try:
            amount = float(request.data.get('amount', 0))
        except (TypeError, ValueError):
            return Response({'error': 'Amount must be a valid number'}, status=status.HTTP_400_BAD_REQUEST)
        if amount <= 0:
            return Response({'error': 'Amount must be greater than 0'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                rfid_account = RFIDAccount.objects.select_for_update().get(rfid_uid=rfid_uid)
                old_balance = rfid_account.balance
                rfid_account.balance += amount
                rfid_account.save()
                Transaction.objects.create(
                    rfid_account=rfid_account,
                    transaction_type='topup',
                    gate_id='topup_counter',
                    old_balance=old_balance,
                    new_balance=rfid_account.balance,
                    amount_changed=amount
                )
        except RFIDAccount.DoesNotExist:
            return Response({'error': 'RFID not found'}, status=status.HTTP_404_NOT_FOUND)

        publish_to_firebase('rfid_data', {
            'rfid_uid': rfid_uid,
            'balance': rfid_account.balance,
            'updated_at': timezone.now().isoformat()
        })
        return Response({
            'message': 'Balance updated successfully',
            'rfid_uid': rfid_uid,
            'old_balance': old_balance,
            'new_balance': rfid_account.balance,
            'amount_added': amount
        })


    @action(detail=False, methods=['get'])
    def all_accounts(self, request):
        accounts = RFIDAccount.objects.all()
        serializer = RFIDAccountSerializer(accounts, many=True)
        return Response(serializer.data)


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    @action(detail=False, methods=['get'])
    def recent(self, request):
        transactions = Transaction.objects.all()[:50]
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_rfid(self, request):
        rfid_uid = request.query_params.get('rfid_uid')
        if not rfid_uid:
            return Response({'error': 'rfid_uid parameter required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            rfid_account = RFIDAccount.objects.get(rfid_uid=rfid_uid)
            transactions = Transaction.objects.filter(rfid_account=rfid_account)
            serializer = TransactionSerializer(transactions, many=True)
            return Response(serializer.data)
        except RFIDAccount.DoesNotExist:
            return Response({'error': 'RFID not found'}, status=status.HTTP_404_NOT_FOUND)


class FloodSensorViewSet(viewsets.ModelViewSet):
    queryset = FloodSensor.objects.all()
    serializer_class = FloodSensorSerializer

    @action(detail=False, methods=['post'])
    def update_level(self, request):
        water_level = float(request.data.get('water_level', 0))
        is_emergency = water_level >= EMERGENCY_WATER_LEVEL
        FloodSensor.objects.create(water_level=water_level, is_emergency=is_emergency)
        publish_to_firebase('flood_sensor', {
            'water_level': water_level,
            'is_emergency': is_emergency,
            'timestamp': timezone.now().isoformat()
        })
        return Response({
            'water_level': water_level,
            'is_emergency': is_emergency,
            'message': 'Emergency evacuation activated!' if is_emergency else 'Water level normal'
        })

    @action(detail=False, methods=['get'])
    def current(self, request):
        latest = FloodSensor.objects.latest('timestamp') if FloodSensor.objects.exists() else None
        if not latest:
            return Response({'error': 'No sensor data available'}, status=status.HTTP_404_NOT_FOUND)
        serializer = FloodSensorSerializer(latest)
        return Response(serializer.data)
