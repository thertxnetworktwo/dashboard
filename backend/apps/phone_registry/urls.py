from django.urls import path
from .views import (
    PhoneCheckView,
    PhoneRegisterView,
    PhoneBulkRegisterView,
    PhoneCleanupView,
    phone_registry_health
)

urlpatterns = [
    path('health/', phone_registry_health, name='phone-registry-health'),
    path('check/', PhoneCheckView.as_view(), name='phone-check'),
    path('register/', PhoneRegisterView.as_view(), name='phone-register'),
    path('bulk-register/', PhoneBulkRegisterView.as_view(), name='phone-bulk-register'),
    path('cleanup/', PhoneCleanupView.as_view(), name='phone-cleanup'),
]
