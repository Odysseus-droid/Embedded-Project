from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RFIDAccountViewSet, TransactionViewSet, FloodSensorViewSet

router = DefaultRouter()
router.register(r'rfid-accounts', RFIDAccountViewSet, basename='rfid-account')
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'flood', FloodSensorViewSet, basename='flood')

urlpatterns = [
    path('', include(router.urls)),
]
