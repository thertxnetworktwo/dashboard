from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    health_check,
    check_phone,
    register_phone,
    bulk_register_phones,
    cleanup_records,
    APICallLogViewSet
)

router = DefaultRouter()
router.register(r'logs', APICallLogViewSet, basename='api-log')

urlpatterns = [
    path('health/', health_check, name='phone-health'),
    path('check/', check_phone, name='phone-check'),
    path('register/', register_phone, name='phone-register'),
    path('bulk-register/', bulk_register_phones, name='phone-bulk-register'),
    path('cleanup/', cleanup_records, name='phone-cleanup'),
    path('', include(router.urls)),
]
