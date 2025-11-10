from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
import logging

from .services import get_phone_registry_service
from .serializers import (
    PhoneCheckSerializer,
    PhoneRegisterSerializer,
    PhoneBulkRegisterSerializer,
    PhoneCleanupSerializer
)

logger = logging.getLogger(__name__)


class PhoneCheckView(APIView):
    """Check if a phone number exists in the registry."""
    
    def post(self, request):
        serializer = PhoneCheckSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        phone_number = serializer.validated_data['phone_number']
        
        try:
            service = get_phone_registry_service()
            result = service.check_phone(phone_number)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error checking phone number: {str(e)}")
            return Response(
                {'error': 'Failed to check phone number', 'detail': str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )


class PhoneRegisterView(APIView):
    """Register a single phone number."""
    
    def post(self, request):
        serializer = PhoneRegisterSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        phone_number = serializer.validated_data['phone_number']
        
        try:
            service = get_phone_registry_service()
            result = service.register_phone(phone_number)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error registering phone number: {str(e)}")
            return Response(
                {'error': 'Failed to register phone number', 'detail': str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )


class PhoneBulkRegisterView(APIView):
    """Register multiple phone numbers."""
    
    def post(self, request):
        serializer = PhoneBulkRegisterSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        phone_numbers = serializer.validated_data['phone_numbers']
        
        try:
            service = get_phone_registry_service()
            result = service.bulk_register(phone_numbers)
            return Response(result, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error bulk registering phone numbers: {str(e)}")
            return Response(
                {'error': 'Failed to bulk register phone numbers', 'detail': str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )


class PhoneCleanupView(APIView):
    """Cleanup old phone registry records."""
    
    def delete(self, request):
        serializer = PhoneCleanupSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        retention_days = serializer.validated_data['retention_days']
        
        try:
            service = get_phone_registry_service()
            result = service.cleanup_old_records(retention_days)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error cleaning up records: {str(e)}")
            return Response(
                {'error': 'Failed to cleanup records', 'detail': str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )


@api_view(['GET'])
def phone_registry_health(request):
    """Get health status of the external phone registry API."""
    try:
        service = get_phone_registry_service()
        health_data = service.check_health(use_cache=True)
        return Response(health_data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error checking health: {str(e)}")
        return Response(
            {'status': 'unhealthy', 'error': str(e)},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )

