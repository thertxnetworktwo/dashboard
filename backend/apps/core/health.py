from django.db import connection
from django.utils import timezone
import logging

from apps.phone_registry.services import get_phone_registry_service

logger = logging.getLogger(__name__)


def check_database():
    """Check if database is connected."""
    try:
        connection.ensure_connection()
        return True, "connected"
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        return False, str(e)


def check_external_api():
    """Check if external phone registry API is available."""
    try:
        service = get_phone_registry_service()
        health_data = service.check_health(use_cache=False)
        
        if health_data.get('status') == 'healthy':
            return True, "connected"
        else:
            return False, health_data.get('error', 'unhealthy')
    except Exception as e:
        logger.error(f"External API health check failed: {str(e)}")
        return False, str(e)


def get_health_status():
    """
    Get overall health status of the application.
    
    Returns:
        Dictionary with health status of database and external API
    """
    db_healthy, db_status = check_database()
    api_healthy, api_status = check_external_api()
    
    overall_status = "healthy" if (db_healthy and api_healthy) else "degraded"
    
    return {
        "status": overall_status,
        "database": db_status,
        "external_api": api_status,
        "timestamp": timezone.now().isoformat()
    }
