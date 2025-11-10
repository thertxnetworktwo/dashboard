from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection
from apps.phone_registry.services import PhoneRegistryAPIService
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


@api_view(['GET'])
def health_check(request):
    """
    Main health check endpoint that checks:
    - Server status
    - Database connection
    - External Phone Registry API connection
    """
    health_status = {
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'database': 'disconnected',
        'external_api': 'disconnected',
    }
    
    # Check database connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            health_status['database'] = 'connected'
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        health_status['database'] = 'disconnected'
        health_status['status'] = 'unhealthy'
    
    # Check external API connection
    try:
        service = PhoneRegistryAPIService()
        external_health = service.check_health()
        
        if external_health.get('status') == 'healthy':
            health_status['external_api'] = 'connected'
        else:
            health_status['external_api'] = 'unhealthy'
            health_status['status'] = 'degraded'
    except Exception as e:
        logger.error(f"External API health check failed: {str(e)}")
        health_status['external_api'] = 'disconnected'
        health_status['status'] = 'degraded'
    
    # Determine overall status code
    if health_status['status'] == 'unhealthy':
        status_code = 503
    elif health_status['status'] == 'degraded':
        status_code = 200  # Still operational even if external API is down
    else:
        status_code = 200
    
    return Response(health_status, status=status_code)
