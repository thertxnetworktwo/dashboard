from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from .services import PhoneRegistryAPIService
from .serializers import (
    PhoneCheckSerializer,
    PhoneRegisterSerializer,
    PhoneBulkRegisterSerializer,
    PhoneCleanupSerializer,
    APICallLogSerializer
)
from .models import APICallLog
import logging

logger = logging.getLogger(__name__)


@api_view(['GET'])
def health_check(request):
    """Check the health status of the external Phone Registry API."""
    try:
        service = PhoneRegistryAPIService()
        health_data = service.check_health()
        
        return Response({
            'external_api': health_data,
            'status': health_data.get('status', 'unknown')
        })
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return Response({
            'external_api': {'status': 'unhealthy', 'error': str(e)},
            'status': 'unhealthy'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['POST'])
def check_phone(request):
    """Check if a phone number exists in the registry."""
    serializer = PhoneCheckSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        service = PhoneRegistryAPIService()
        result = service.check_phone(serializer.validated_data['phone_number'])
        
        return Response(result)
    except Exception as e:
        logger.error(f"Check phone failed: {str(e)}")
        return Response({
            'error': 'Failed to check phone number',
            'details': str(e)
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['POST'])
def register_phone(request):
    """Register a single phone number."""
    serializer = PhoneRegisterSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        service = PhoneRegistryAPIService()
        result = service.register_phone(serializer.validated_data['phone_number'])
        
        return Response(result, status=status.HTTP_201_CREATED)
    except Exception as e:
        logger.error(f"Register phone failed: {str(e)}")
        return Response({
            'error': 'Failed to register phone number',
            'details': str(e)
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['POST'])
def bulk_register_phones(request):
    """Register multiple phone numbers (up to 1000)."""
    serializer = PhoneBulkRegisterSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        service = PhoneRegistryAPIService()
        result = service.bulk_register(serializer.validated_data['phone_numbers'])
        
        return Response(result, status=status.HTTP_201_CREATED)
    except ValueError as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Bulk register failed: {str(e)}")
        return Response({
            'error': 'Failed to bulk register phone numbers',
            'details': str(e)
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['POST'])
def cleanup_records(request):
    """Delete records older than retention period."""
    serializer = PhoneCleanupSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        service = PhoneRegistryAPIService()
        result = service.cleanup_old_records(serializer.validated_data['retention_days'])
        
        return Response(result)
    except Exception as e:
        logger.error(f"Cleanup failed: {str(e)}")
        return Response({
            'error': 'Failed to cleanup records',
            'details': str(e)
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class APICallLogViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing API call logs."""
    
    queryset = APICallLog.objects.all()
    serializer_class = APICallLogSerializer
    
    def get_queryset(self):
        """Filter queryset based on query parameters."""
        queryset = super().get_queryset()
        
        # Filter by endpoint
        endpoint = self.request.query_params.get('endpoint', None)
        if endpoint:
            queryset = queryset.filter(endpoint__icontains=endpoint)
        
        # Filter by success status
        success = self.request.query_params.get('success', None)
        if success is not None:
            queryset = queryset.filter(success=success.lower() == 'true')
        
        return queryset
