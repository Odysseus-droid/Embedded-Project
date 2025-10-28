from django.urls import path, include
from rest_framework.routers import DefaultRouter
from toll_system.views import (
    RFIDAccountViewSet,
    TransactionViewSet,
    FloodSensorViewSet,
    DashboardView,
    RFIDListView,
    RFIDDetailView,
    TransactionListView,
    SystemStatusView,
    StatusView,
    home
)

router = DefaultRouter()
router.register(r'rfid-accounts', RFIDAccountViewSet, basename='rfid-account')
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'flood', FloodSensorViewSet, basename='flood')

urlpatterns = [
    # API endpoints using DRF viewsets
    path('api/', include(router.urls)),

    # Custom API actions
    path('api/rfid-accounts/topup/', RFIDAccountViewSet.as_view({'post': 'topup'}), name='rfid-topup'),
    path('api/rfid-accounts/all_accounts/', RFIDAccountViewSet.as_view({'get': 'all_accounts'}), name='rfid-all-accounts'),

    # Frontend/views
    path('status/', StatusView.as_view(), name='status'),
    path('', home, name='home'),
    path('rfid-accounts/', RFIDListView.as_view(), name='rfid_list'),
    path('rfid-accounts/<str:rfid_uid>/', RFIDDetailView.as_view(), name='rfid_detail'),
    path('transactions/', TransactionListView.as_view(), name='transaction_list'),
    path('system-status/', SystemStatusView.as_view(), name='system_status'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
