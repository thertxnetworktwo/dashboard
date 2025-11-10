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
    PhoneListSerializer,
    PhoneAnalyticsSerializer,
    PhoneCleanupSerializer,
    SpamAnalysisSerializer,
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
    """Register a single phone number with full details."""
    
    def post(self, request):
        serializer = PhoneRegisterSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            service = get_phone_registry_service()
            result = service.register_phone(
                phone_number=serializer.validated_data['phone_number'],
                botname=serializer.validated_data['botname'],
                country=serializer.validated_data['country'],
                iso2=serializer.validated_data['iso2'],
                twofa=serializer.validated_data['twofa'],
                session_string=serializer.validated_data['session_string'],
                quality=serializer.validated_data.get('quality'),
            )
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


class PhoneListView(APIView):
    """List phone numbers with pagination and filtering."""
    
    def get(self, request):
        serializer = PhoneListSerializer(data=request.query_params)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            service = get_phone_registry_service()
            result = service.list_phones(
                page=serializer.validated_data.get('page', 1),
                limit=serializer.validated_data.get('limit', 100),
                botname=serializer.validated_data.get('botname'),
                country=serializer.validated_data.get('country'),
                iso2=serializer.validated_data.get('iso2'),
                is_bulked=serializer.validated_data.get('is_bulked'),
                quality=serializer.validated_data.get('quality'),
                order_by=serializer.validated_data.get('order_by', 'registered_at'),
                order_direction=serializer.validated_data.get('order_direction', 'desc'),
            )
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error listing phone numbers: {str(e)}")
            return Response(
                {'error': 'Failed to list phone numbers', 'detail': str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )


class PhoneAnalyticsView(APIView):
    """Get analytics and statistics for phone registry."""
    
    def get(self, request):
        serializer = PhoneAnalyticsSerializer(data=request.query_params)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            service = get_phone_registry_service()
            result = service.get_analytics(
                start_date=serializer.validated_data.get('start_date'),
                end_date=serializer.validated_data.get('end_date'),
                is_bulked=serializer.validated_data.get('is_bulked'),
            )
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error getting analytics: {str(e)}")
            return Response(
                {'error': 'Failed to get analytics', 'detail': str(e)},
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


class SpamAnalysisView(APIView):
    """Analyze message for spam/account status detection."""
    
    def post(self, request):
        serializer = SpamAnalysisSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        message = serializer.validated_data['message']
        
        try:
            service = get_phone_registry_service()
            result = service.analyze_spam(message)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error analyzing spam: {str(e)}")
            return Response(
                {'error': 'Failed to analyze spam', 'detail': str(e)},
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

