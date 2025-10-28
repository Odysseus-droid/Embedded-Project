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
    # API endpoints using DRF router
    path('api/', include(router.urls)),

    # Custom DRF actions must come BEFORE the detail path
    path('api/rfid-accounts/all_accounts/', RFIDAccountViewSet.as_view({'get': 'all_accounts'}), name='rfid-all-accounts'),
    path('api/rfid-accounts/topup/', RFIDAccountViewSet.as_view({'post': 'topup'}), name='rfid-topup'),

    # Frontend/views
    path('status/', StatusView.as_view(), name='status'),
    path('', home, name='home'),

    # Detail path must be after any conflicting paths
    path('rfid-accounts/<str:rfid_uid>/', RFIDDetailView.as_view(), name='rfid_detail'),
    path('rfid-accounts/', RFIDListView.as_view(), name='rfid_list'),

    path('transactions/', TransactionListView.as_view(), name='transaction_list'),
    path('system-status/', SystemStatusView.as_view(), name='system_status'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
