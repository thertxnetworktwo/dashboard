import requests
import logging
import time
from typing import Dict, List, Optional, Any
from django.conf import settings
from django.core.cache import cache
from .models import APICallLog
from .utils import retry_with_backoff

logger = logging.getLogger(__name__)


class PhoneRegistryAPIService:
    """Service class to interact with the external Phone Registry API."""
    
    def __init__(self):
        self.base_url = settings.PHONE_REGISTRY_API_URL.rstrip('/')
        self.api_key = settings.PHONE_REGISTRY_API_KEY
        self.timeout = settings.PHONE_REGISTRY_API_TIMEOUT
        self.headers = {
            'X-API-Key': self.api_key,
            'Content-Type': 'application/json',
        }
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        log_call: bool = True
    ) -> Dict[str, Any]:
        """
        Make an HTTP request to the external API with error handling and logging.
        
        Args:
            method: HTTP method (GET, POST, DELETE)
            endpoint: API endpoint path
            data: Request payload
            log_call: Whether to log this API call
        
        Returns:
            Response data as dictionary
        
        Raises:
            requests.RequestException: If the request fails
        """
        url = f"{self.base_url}{endpoint}"
        start_time = time.time()
        
        try:
            response = requests.request(
                method=method,
                url=url,
                json=data,
                headers=self.headers,
                timeout=self.timeout
            )
            
            response_time_ms = int((time.time() - start_time) * 1000)
            
            # Try to parse JSON response
            try:
                response_data = response.json()
            except ValueError:
                response_data = {'raw': response.text}
            
            # Log the API call
            if log_call:
                APICallLog.objects.create(
                    endpoint=endpoint,
                    method=method,
                    request_data=data,
                    response_data=response_data,
                    status_code=response.status_code,
                    success=response.status_code < 400,
                    response_time_ms=response_time_ms
                )
            
            # Raise exception for bad status codes
            response.raise_for_status()
            
            logger.info(f"API call successful: {method} {endpoint} - {response.status_code}")
            return response_data
            
        except requests.exceptions.Timeout as e:
            response_time_ms = int((time.time() - start_time) * 1000)
            error_msg = f"Request timeout after {self.timeout}s"
            
            if log_call:
                APICallLog.objects.create(
                    endpoint=endpoint,
                    method=method,
                    request_data=data,
                    success=False,
                    error_message=error_msg,
                    response_time_ms=response_time_ms
                )
            
            logger.error(f"API timeout: {method} {endpoint} - {error_msg}")
            raise
            
        except requests.exceptions.RequestException as e:
            response_time_ms = int((time.time() - start_time) * 1000)
            error_msg = str(e)
            status_code = getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None
            
            if log_call:
                APICallLog.objects.create(
                    endpoint=endpoint,
                    method=method,
                    request_data=data,
                    status_code=status_code,
                    success=False,
                    error_message=error_msg,
                    response_time_ms=response_time_ms
                )
            
            logger.error(f"API error: {method} {endpoint} - {error_msg}")
            raise
    
    @retry_with_backoff(max_retries=3)
    def check_health(self) -> Dict[str, Any]:
        """
        Check the health status of the external API.
        Uses caching to avoid excessive health checks.
        
        Returns:
            Health status data
        """
        cache_key = 'phone_registry_health'
        cached_health = cache.get(cache_key)
        
        if cached_health is not None:
            logger.debug("Returning cached health status")
            return cached_health
        
        try:
            health_data = self._make_request('GET', '/health', log_call=False)
            
            # Cache for 5 minutes
            cache.set(cache_key, health_data, 300)
            
            return health_data
            
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return {
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': time.time()
            }
    
    @retry_with_backoff(max_retries=3)
    def check_phone(self, phone_number: str) -> Dict[str, Any]:
        """
        Check if a phone number exists in the registry.
        
        Args:
            phone_number: Phone number to check (e.g., "+1234567890")
        
        Returns:
            Check result with existence status and registration timestamp
        """
        return self._make_request(
            'POST',
            '/api/phone/check',
            data={'phone_number': phone_number}
        )
    
    @retry_with_backoff(max_retries=3)
    def register_phone(self, phone_number: str) -> Dict[str, Any]:
        """
        Register a single phone number.
        
        Args:
            phone_number: Phone number to register (e.g., "+1234567890")
        
        Returns:
            Registration result
        """
        return self._make_request(
            'POST',
            '/api/phone/register',
            data={'phone_number': phone_number}
        )
    
    @retry_with_backoff(max_retries=3)
    def bulk_register(self, phone_numbers: List[str]) -> Dict[str, Any]:
        """
        Register multiple phone numbers (up to 1000).
        
        Args:
            phone_numbers: List of phone numbers to register
        
        Returns:
            Bulk registration results with counts
        """
        if len(phone_numbers) > 1000:
            raise ValueError("Cannot register more than 1000 phone numbers at once")
        
        return self._make_request(
            'POST',
            '/api/phone/bulk-register',
            data={'phone_numbers': phone_numbers}
        )
    
    @retry_with_backoff(max_retries=3)
    def cleanup_old_records(self, retention_days: int) -> Dict[str, Any]:
        """
        Delete records older than the specified retention period.
        
        Args:
            retention_days: Number of days to retain records
        
        Returns:
            Cleanup results with deletion count
        """
        return self._make_request(
            'DELETE',
            '/api/phone/cleanup',
            data={'retention_days': retention_days}
        )
